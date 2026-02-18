# GitHub Actions Fundamentals

GitHub Actions automates CI/CD using workflows in `.github/workflows/*.yml`.

## Core Concepts

- `Workflow`: Automation file triggered by events.
- `Job`: Group of steps running on a runner.
- `Step`: Command or reusable action.
- `Action`: Reusable task package.
- `Runner`: Execution environment (GitHub-hosted/self-hosted).

## Best Practices

- Trigger minimally (`push`, `pull_request`, tags).
- Pin action versions.
- Use matrix builds for compatibility testing.
- Store secrets in repository/environment secrets.
- Fail fast on lint/test/security checks.
