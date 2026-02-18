# Terraform Fundamentals

Terraform manages infrastructure declaratively with execution plans and state.

## Core Concepts

- Providers and resources
- State file and backend
- Variables, outputs, and locals
- Modules for reuse

## Common Workflow

```bash
terraform init
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
```

## Best Practices

- Use remote state with locking.
- Structure reusable modules.
- Enforce review for plan output before apply.
