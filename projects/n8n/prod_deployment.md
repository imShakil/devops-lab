# n8n Production Deployment Guide

Stack: Postgres 16 + Redis 7 + n8n (queue mode, main + workers) + task runner sidecars + Nginx.

## 1. Prerequisites

| Requirement | Notes |
|---|---|
| Docker Engine | 24+ |
| Docker Compose | v2 (`docker compose`, not `docker-compose`) — needed for `deploy.replicas` support outside Swarm |
| Domain + DNS | A record pointing at the host, for `N8N_HOST` |
| TLS certs | Not automated in this stack — see §6 |

## 2. First-time setup

```bash
cp .env.example .env
openssl rand -base64 24    # run 3x — POSTGRES_PASSWORD, POSTGRES_NON_ROOT_PASSWORD, REDIS_PASSWORD
openssl rand -hex 32       # run 2x — N8N_ENCRYPTION_KEY, N8N_RUNNERS_AUTH_TOKEN
```

Fill every value into `.env`. Set `N8N_HOST` and `WEBHOOK_URL` to your real domain.

**Immediately back up `N8N_ENCRYPTION_KEY` somewhere outside this host** (password manager, secrets vault). If it's lost, every credential stored in n8n becomes permanently undecryptable — there is no recovery path.

## 3. `init-data.sh`

Required by the `postgres` service to create the non-root app user. Place next to `docker-compose.yml`:

```bash
#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER $POSTGRES_NON_ROOT_USER WITH PASSWORD '$POSTGRES_NON_ROOT_PASSWORD';
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_NON_ROOT_USER;
EOSQL
```

## 4. Nginx config

Not included in this repo — you'll need `nginx/nginx.conf` and certs under `nginx/ssl/`. Minimum requirements for the upstream block:

- `proxy_pass http://n8n:5678;`
- Websocket upgrade headers (`Upgrade`/`Connection`) — n8n's editor UI relies on this for live updates
- `client_max_body_size` raised if you handle large binary data / file uploads

## 5. Start the stack

```bash
docker compose up -d
docker compose ps                 # all services should report healthy
docker compose logs -f n8n        # watch main app boot
```

First boot creates an owner account at `https://<N8N_HOST>/setup`.

## 6. TLS certificates

Two common options — pick one, neither is wired up automatically:

| Option | Approach |
|---|---|
| Certbot sidecar | Add a `certbot` service + webroot volume shared with nginx, cron renewal via `docker compose run` |
| External reverse proxy | Put Traefik/Caddy in front instead of raw nginx if you want auto-renewal built in |

## 7. Scaling workers

```bash
# edit .env
N8N_WORKER_REPLICAS=4
docker compose up -d --scale n8n-worker=4 --scale n8n-worker-runner=4
```

Keep `n8n-worker` and `n8n-worker-runner` replica counts equal — each worker needs its own runner for Code node execution.

## 8. Backups

| Data | Method | Frequency |
|---|---|---|
| Postgres (workflows, credentials, executions) | `docker compose exec postgres pg_dump -U $POSTGRES_NON_ROOT_USER $POSTGRES_DB > backup.sql`, ship offsite (S3/rsync) | Daily |
| `n8n_data` volume (binary data, community nodes) | Volume snapshot or `tar` | Weekly |
| `N8N_ENCRYPTION_KEY` | Secrets vault, separate from above | Once, verify yearly |

Restoring credentials requires the **same** `N8N_ENCRYPTION_KEY` that encrypted them — a Postgres restore alone is not sufficient.

## 9. Health checks

```bash
docker compose ps                                  # container-level health
curl -f https://<N8N_HOST>/healthz                  # app-level
docker compose exec redis redis-cli -a $REDIS_PASSWORD ping
docker compose exec postgres pg_isready -U $POSTGRES_USER
```

## 10. Common issues

| Symptom | Likely cause |
|---|---|
| Workers not picking up jobs | `QUEUE_BULL_REDIS_PASSWORD` mismatch between `n8n` and `n8n-worker`, or Redis not healthy yet |
| Code node executions fail with runner errors | Runner image tag doesn't match n8n image tag exactly, or `N8N_RUNNERS_AUTH_TOKEN` mismatch |
| `n8n-worker` won't scale past 1 | Leftover `container_name` on the service — must be absent for `replicas` to work |
| Editor UI freezes / no live updates | Nginx missing websocket upgrade headers |
| Executions table growing unbounded | `EXECUTIONS_DATA_PRUNE` not applied — check env is actually loaded (`docker compose exec n8n env \| grep EXECUTIONS`) |

## 11. Version upgrades

1. Bump `x-n8n-image` **and** `x-runner-image` tags to the same version together — never let them drift apart.
2. Check n8n's release notes for breaking changes to env vars.
3. `docker compose pull && docker compose up -d`
4. Postgres migrations run automatically on `n8n` container start.
