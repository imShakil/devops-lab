# Flux CD Fundamentals

Flux continuously reconciles Kubernetes manifests and Helm releases from Git.

## Core Concepts

- `Source` objects (GitRepository/HelmRepository).
- `Kustomization` for applying manifests.
- `HelmRelease` for Helm-driven deployments.
- Reconciliation loops for drift correction.

## Best Practices

- Split source and environment overlays.
- Use image automation only with guarded policies.
- Monitor reconciliation and suspend resources during incident response.
