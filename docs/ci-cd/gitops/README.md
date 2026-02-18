# GitOps Fundamentals

GitOps uses Git as the single source of truth for infrastructure and app deployment state.

## Core Concepts

- Declarative manifests stored in Git.
- Pull-based reconciliation from cluster agents.
- Continuous drift detection and self-healing.
- Auditable change history through commits/PRs.

## Tools in this folder

- `argoCD/`
- `fluxCD/`

## Best Practices

- Keep app and platform repos clearly separated.
- Enforce PR reviews before merges.
- Use environment overlays/branches consistently.
- Alert on reconciliation failures and drift.
