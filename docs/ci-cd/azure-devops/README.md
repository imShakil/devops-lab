# Azure DevOps Pipelines Fundamentals

Azure Pipelines automates builds, tests, and deployments with YAML pipelines.

## Core Concepts

- `Pipeline`: End-to-end CI/CD definition.
- `Stage`: Environment-level boundary.
- `Job`: Unit running on an agent.
- `Task`: Built-in operation in a job.
- `Service Connection`: Secure integration to cloud/tools.

## Best Practices

- Use multi-stage YAML for environment promotion.
- Protect branches and require PR validation.
- Use variable groups and key vault integration.
- Separate infra and application deployment concerns.
