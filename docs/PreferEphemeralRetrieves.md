# Prefer Ephemeral Resources for Data Retrieval

| Category | Resource Types | Severity |
|----------|---------------|----------|
| Security | Multiple Providers | MEDIUM |

## Description

This policy checks if data sources that retrieve secret values are using ephemeral alternatives.

When a data source has an ephemeral alternative available, you should use the ephemeral data source instead to avoid storing sensitive data in the Terraform state file. Ephemeral data sources are designed to handle sensitive data more securely by not persisting it in state.

## Remediation

Replace non-ephemeral data sources with their ephemeral alternatives when retrieving sensitive information.

### Example

Instead of:
```hcl
data "aws_ssm_parameter" "example" {
  name = "/example/parameter"
}
```

Use:
```hcl
data "aws_secretsmanager_random_password" "example" {
  exclude_lowercase = false
  exclude_numbers   = true
  exclude_punctuation = true
  exclude_uppercase = false
  include_space     = false
  length            = 16
}
```

## Terraform Version Compatibility

This policy is designed to work with Terraform 1.11 and later, as ephemeral resources were introduced in Terraform 1.11. The policy will automatically skip checks for earlier versions of Terraform when possible.
