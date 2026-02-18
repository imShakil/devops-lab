# Jenkins Fundamentals

Jenkins is an automation server for CI/CD pipelines.

## Core Concepts

- `Job`: Unit of automation (freestyle or pipeline).
- `Pipeline`: Declarative/scripted workflow in `Jenkinsfile`.
- `Agent`: Worker node that executes stages.
- `Plugin`: Extension for integrations and features.
- `Credentials`: Secure secret management for pipelines.

## Best Practices

- Prefer pipeline-as-code (`Jenkinsfile`).
- Keep controller lightweight, run workloads on agents.
- Version and backup Jenkins configuration.
- Restrict plugin usage to trusted/maintained plugins.
- Implement role-based access control.
