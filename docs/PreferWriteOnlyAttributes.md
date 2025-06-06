# Prefer Write-Only Resource Attributes

| Category | Resource Types | Severity |
|----------|---------------|----------|
| Security | Multiple Providers | MEDIUM |

## Description

This policy checks if resources with write-only attribute options are using them.

Write-only attributes are designed to handle sensitive data more securely by not persisting it in state. When a resource has a write-only attribute available, you should use it instead of the regular attribute to avoid storing sensitive data in the Terraform state file.

## Remediation

Use write-only attributes when available for resources that handle sensitive information.

### Example

Instead of:
```hcl
resource "aws_ssm_parameter" "example" {
  name  = "/example/parameter"
  type  = "SecureString"
  value = "sensitive-value"  # Stores the value in state
}
```

Use:
```hcl
resource "aws_ssm_parameter" "example" {
  name     = "/example/parameter"
  type     = "SecureString"
  value_wo = "sensitive-value"  # Does not store the value in state
}
```

## Terraform Version Compatibility

This policy is designed to work with Terraform 1.11 and later, as write-only attributes were introduced in Terraform 1.11. The policy will automatically skip checks for earlier versions of Terraform when possible.
