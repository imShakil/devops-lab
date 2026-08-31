# n8n Production Deployment Guide

Stack: Postgres 16 + Redis 8 + n8n (queue mode, main + one worker) + task runner sidecar. TLS is not in Compose — bind is `127.0.0.1:5678`.

## 1. Prerequisites

| Requirement | Notes |
| --- | --- |
| Docker Engine | 24+ |
| Docker Compose | v2 (`docker compose`, not `docker-compose`) |
| Domain + DNS | A record pointing at the host, for `N8N_HOST` (only if exposing publicly) |
| Host reverse proxy | Caddy / nginx / Traefik on the host for HTTPS → `http://127.0.0.1:5678` |

## 2. First-time setup

```bash
cp .env.example .env
openssl rand -base64 24    # run 3x — POSTGRES_PASSWORD, POSTGRES_NON_ROOT_PASSWORD, REDIS_PASSWORD
openssl rand -hex 32       # run 2x — N8N_ENCRYPTION_KEY, N8N_RUNNERS_AUTH_TOKEN
```

Fill every value into `.env`. Set `N8N_HOST` and `WEBHOOK_URL` to your real domain.

**Immediately back up `N8N_ENCRYPTION_KEY` somewhere outside this host** (password manager, secrets vault). If it's lost, every credential stored in n8n becomes permanently undecryptable — there is no recovery path.

## 3. `init-data.sh`

Ships in this directory and is mounted by the `postgres` service to create the non-root user n8n connects as.

It runs **only on an empty data directory**. Editing it after the first boot has no effect — see §10 if migrations already failed.

Postgres 15+ revoked `CREATE` on schema `public` from `PUBLIC`, so the script also transfers schema ownership. Granting privileges on the database alone is not enough and n8n's migrations fail with `permission denied for schema public`.

## 4. Ingress (host reverse proxy)

n8n listens on **HTTP** `127.0.0.1:5678` only. It is not reachable from other machines unless you proxy it.

Local editor: `http://127.0.0.1:5678`

Public access: terminate TLS on the host and proxy to `http://127.0.0.1:5678`. The proxy must:

- Upgrade websockets (`Upgrade` / `Connection`) — the editor UI needs this
- Raise `client_max_body_size` / equivalent if you upload large files
- Forward `Host` and `X-Forwarded-*` (Compose already sets `N8N_TRUST_PROXY` / `N8N_PROXY_HOPS=1`)

Set `N8N_PROTOCOL=https` and `WEBHOOK_URL=https://<N8N_HOST>/` to the **public** URL, not localhost.

Local-only (no proxy): `N8N_PROTOCOL=http` and `WEBHOOK_URL=http://127.0.0.1:5678/`.

## 5. Start the stack

```bash
docker compose up -d
docker compose ps                 # all services should report healthy
docker compose logs -f n8n        # watch main app boot
```

First boot creates an owner account at `http://127.0.0.1:5678/setup` (or `https://<N8N_HOST>/setup` once the host proxy is up).

## 6. TLS certificates

TLS is a host concern, not this Compose file. Typical options:

| Option | Approach |
| --- | --- |
| Caddy / Traefik on the host | Auto-HTTPS, reverse proxy to `127.0.0.1:5678` |
| Host nginx + Certbot | Same upstream; websocket headers required |

## 7. Scaling workers

Do not use Compose `replicas` or `--scale` for `n8n-worker` / `n8n-worker-runner`. The runner connects to `http://n8n-worker:5679`; with multiple replicas Compose DNS round-robins, so Code nodes can hit a worker that has no runner attached.

This stack is one worker + one runner. Raise throughput with `worker --concurrency=…` first. Extra workers need separately named services, each with its own runner pointing at that service hostname.

## 8. Backups

| Data | Method | Frequency |
| --- | --- | --- |
| Postgres (workflows, credentials, executions) | `docker compose exec postgres pg_dump -U $POSTGRES_NON_ROOT_USER $POSTGRES_DB > backup.sql`, ship offsite (S3/rsync) | Daily |
| `n8n_data` volume (binary data, community nodes) | Volume snapshot or `tar` | Weekly |
| `N8N_ENCRYPTION_KEY` | Secrets vault, separate from above | Once, verify yearly |

Restoring credentials requires the **same** `N8N_ENCRYPTION_KEY` that encrypted them — a Postgres restore alone is not sufficient.

## 9. Health checks

```bash
docker compose ps                                  # container-level health
curl -f http://127.0.0.1:5678/healthz               # app-level (or https://<N8N_HOST>/healthz via proxy)
docker compose exec redis redis-cli -a $REDIS_PASSWORD ping
docker compose exec postgres pg_isready -U $POSTGRES_USER
```

## 10. Common issues

| Symptom | Likely cause |
| --- | --- |
| Workers not picking up jobs | `QUEUE_BULL_REDIS_PASSWORD` mismatch between `n8n` and `n8n-worker`, or Redis not healthy yet |
| Code node executions fail with runner errors | Runner image tag doesn't match n8n image tag exactly, or `N8N_RUNNERS_AUTH_TOKEN` mismatch |
| Editor UI freezes / no live updates | Host proxy missing websocket upgrade headers |
| Cannot reach n8n from another machine | Expected — port is bound to 127.0.0.1; put a proxy in front |
| Executions table growing unbounded | `EXECUTIONS_DATA_PRUNE` not applied — check env is actually loaded (`docker compose exec n8n env \| grep EXECUTIONS`) |

### `permission denied for schema public`

n8n's migrations cannot create tables. The app user has database privileges but not schema `public` rights (Postgres 15+ behaviour), usually because `init-data.sh` was missing or incomplete when the volume was first created.

Since init scripts do not re-run, fix the live database:

```bash
docker compose exec -e PGPASSWORD=$POSTGRES_PASSWORD postgres \
  psql -U $POSTGRES_USER -d $POSTGRES_DB \
  -c "ALTER SCHEMA public OWNER TO \"$POSTGRES_NON_ROOT_USER\";" \
  -c "GRANT ALL ON SCHEMA public TO \"$POSTGRES_NON_ROOT_USER\";"

docker compose restart n8n n8n-worker
```

Alternatively, on a stack with no data worth keeping, wipe the volume so the corrected script runs from scratch: `docker compose down -v && docker compose up -d`.

## 11. Version upgrades

1. Bump `x-n8n-image` **and** `x-runner-image` tags to the same version together — never let them drift apart.
2. Check n8n's release notes for breaking changes to env vars.
3. `docker compose pull && docker compose up -d`
4. Postgres migrations run automatically on `n8n` container start.
