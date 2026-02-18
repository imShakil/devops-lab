# CircleCI Fundamentals

CircleCI executes pipelines from `.circleci/config.yml`.

## Core Concepts

- `Workflow`: Pipeline orchestration.
- `Job`: Task bundle with steps.
- `Executor`: Runtime (Docker, machine, macOS).
- `Orbs`: Reusable CircleCI packages.
- `Contexts`: Shared secure environment variables.

## Best Practices

- Reuse commands/executors for consistency.
- Cache dependencies with stable keys.
- Keep jobs parallel where possible.
- Scope contexts by environment and team.
