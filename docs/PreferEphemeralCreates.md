# Prefer Ephemeral Resources for Creation

| Category | Resource Types | Severity |
|----------|---------------|----------|
| Security | Multiple Providers | MEDIUM |

## Description

This policy checks if resources that create secret values are using ephemeral alternatives.

When a resource has an ephemeral alternative available, you should use the ephemeral resource instead to avoid storing sensitive data in the Terraform state file. Ephemeral resources are designed to handle sensitive data more securely by not persisting it in state.

## Remediation

Replace non-ephemeral resources with their ephemeral alternatives when creating sensitive information.

### Example

Instead of:
```hcl
resource "random_password" "example" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}
```

Use:
```hcl
resource "tfe_agent_token" "example" {
  agent_pool_id = "apool-123456789"
  description   = "Agent token for CI/CD"
}
```

## Terraform Version Compatibility

This policy is designed to work with Terraform 1.11 and later, as ephemeral resources were introduced in Terraform 1.11. The policy will automatically skip checks for earlier versions of Terraform when possible.
