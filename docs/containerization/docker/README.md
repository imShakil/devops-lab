# Docker Fundamentals

Docker packages applications with their runtime dependencies into portable containers.

## Core Concepts

- `Image`: Immutable template used to create containers.
- `Container`: Running instance of an image.
- `Dockerfile`: Build recipe for an image.
- `Registry`: Image storage (Docker Hub, ECR, GCR, etc.).
- `Volume`: Persistent data outside container lifecycle.
- `Network`: Communication layer between containers/services.

## Basic Workflow

1. Write a `Dockerfile`.
2. Build an image with `docker build`.
3. Run containers with `docker run`.
4. Push image to a registry.
5. Deploy using Compose/Kubernetes/CI pipeline.

## Essential Commands

```bash
docker build -t myapp:1.0 .
docker run -d -p 8080:80 --name myapp myapp:1.0
docker ps
docker logs myapp
docker exec -it myapp sh
docker stop myapp && docker rm myapp
```

## Best Practices

- Use small base images (`alpine`, `distroless` where possible).
- Keep images immutable and version-tagged.
- Avoid storing secrets in images.
- Use multi-stage builds for smaller production images.
- Run containers as non-root users.
