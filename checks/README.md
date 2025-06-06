# Custom Checkov Checks for Ephemerality

This directory contains the implementation of custom Checkov policies that enforce best practices around ephemeral resources and write-only attributes in Terraform configurations.

## Check Implementations

### PreferEphemeralCreates.py
**Check ID:** `CKV2_EPH_CREATE`

This check identifies Terraform resources that create ephemeral data (secrets, tokens, temporary credentials) and suggests using ephemeral data sources instead. The check helps improve security by reducing sensitive data exposure in state files.

**Key Features:**
- Scans all resource types for ephemeral creation patterns
- Uses configurable data from `../data/ephemerality.json`
- Provides actionable recommendations for ephemeral alternatives
- Supports Terraform version-specific logic

### PreferEphemeralRetrieves.py
**Check ID:** `CKV2_EPH_RET`

This check detects data sources that retrieve sensitive or temporary information and recommends marking them as ephemeral to prevent storage in state files.

**Key Features:**
- Focuses on data source configurations
- Identifies retrieval patterns that should be ephemeral
- Helps prevent sensitive data leakage through state files
- Configurable through data files

### PreferWriteOnlyAttributes.py
**Check ID:** `CKV2_EPH_WO`

This check flags sensitive resource attributes that should be configured as write-only to prevent them from being stored in or read from the Terraform state file.

**Key Features:**
- Scans resource attributes for write-only candidates
- Uses detailed configuration from `../data/write-only/` directory
- Helps identify attributes that expose sensitive information
- Supports multiple cloud providers and resource types

## Shared Utilities

### data_loader.py
Contains shared utility functions used across all checks:

- `load_ephemerality_data()` - Loads resource classifications from JSON files
- `get_terraform_version_from_plan()` - Extracts Terraform version information
- `should_skip_check()` - Determines if checks should be skipped based on version
- Error handling and fallback mechanisms for data loading

## Configuration Data

The checks rely on configuration data stored in the `../data/` directory:

- **ephemerality.json** - Master list of resources categorized by ephemerality characteristics
- **ephemeral/** - Detailed configurations for ephemeral resource patterns
- **write-only/** - Attribute definitions organized by resource type

## Development Guidelines

When modifying or extending these checks:

1. **Maintain backward compatibility** - Ensure changes don't break existing functionality
2. **Update data files** - Add new resources/attributes to appropriate configuration files
3. **Test thoroughly** - Add test cases in `../tests/` for new functionality
4. **Follow naming conventions** - Use consistent naming patterns for check IDs and classes
5. **Document changes** - Update relevant documentation and comments

## Error Handling

All checks include robust error handling:
- Graceful fallbacks for missing data files
- Import error handling for module dependencies
- Safe data access with default values
- Logging for debugging and troubleshooting

## Performance Considerations

The checks are designed for efficiency:
- Data is loaded once during initialization
- Minimal resource scanning overhead
- Optimized pattern matching
- Configurable skip conditions

## Credits

These implementations are inspired by and build upon the foundational work from [drewmullen/policy-library-ephemerality](https://github.com/drewmullen/policy-library-ephemerality). The original concepts and approach to ephemerality in Terraform configurations provided the basis for these enhanced Checkov implementations.
