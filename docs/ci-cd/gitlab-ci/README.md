# GitLab CI Fundamentals

GitLab CI runs automated pipelines defined in `.gitlab-ci.yml`.

## Core Concepts

- `Pipeline`: Full CI/CD execution for a commit or merge request.
- `Stage`: Logical phase (`build`, `test`, `deploy`).
- `Job`: Individual task executed by a runner.
- `Runner`: Agent that executes jobs.
- `Artifacts`: Files passed between jobs/stages.
- `Variables`: Config/secrets used by jobs.

## Basic `.gitlab-ci.yml` Shape

```yaml
stages: [build, test, deploy]

build:
  stage: build
  script:
    - echo "build"

test:
  stage: test
  script:
    - echo "test"

deploy:
  stage: deploy
  script:
    - echo "deploy"
  only:
    - main
```

## Best Practices

- Keep jobs fast and deterministic.
- Cache dependencies carefully.
- Use protected branches and protected variables.
- Separate environments (`dev`, `staging`, `prod`).
- Add security scans (SAST/Dependency/Container scanning).
