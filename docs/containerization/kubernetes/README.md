# Kubernetes Fundamentals

Kubernetes orchestrates containers across a cluster with automation for deployment, scaling, and recovery.

## Core Concepts

- `Cluster`: Control plane + worker nodes.
- `Pod`: Smallest deployable unit (one or more containers).
- `Deployment`: Declarative rollout and replica management.
- `Service`: Stable networking endpoint for pods.
- `ConfigMap` and `Secret`: Externalized app configuration.
- `Namespace`: Logical isolation inside a cluster.

## Basic Workflow

1. Package app as a container image.
2. Define manifests (`Deployment`, `Service`).
3. Apply manifests with `kubectl apply`.
4. Observe rollout and pod health.
5. Scale/update declaratively.

## Essential Commands

```bash
kubectl get nodes
kubectl get pods -A
kubectl apply -f deployment.yaml
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl rollout status deployment/<name>
```

## Best Practices

- Use readiness/liveness probes.
- Set CPU and memory requests/limits.
- Store sensitive data in `Secret` objects.
- Use namespaces and RBAC for access control.
- Prefer rolling updates with rollback strategy.
