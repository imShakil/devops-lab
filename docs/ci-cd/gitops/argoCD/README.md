# Argo CD Fundamentals

Argo CD is a Kubernetes GitOps controller that syncs cluster state from Git.

## Core Concepts

- `Application`: Argo CD custom resource mapping Git path to cluster target.
- `Sync`: Applies desired state to cluster.
- `Health`: Resource status evaluation.
- `Project`: Multi-tenant policy boundary for apps/repos/clusters.

## Best Practices

- Use automatic sync with safe sync policies.
- Restrict source repos and destination namespaces via projects.
- Integrate SSO and RBAC.
