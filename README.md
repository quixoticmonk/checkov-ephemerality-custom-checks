# Checkov custom checks: Ephemerality Checks

[![Generate and Test](https://github.com/quixoticmonk/checkov-ephemerality-custom-checks/actions/workflows/generate.yml/badge.svg)](https://github.com/quixoticmonk/checkov-ephemerality-custom-checks/actions/workflows/generate.yml)

This repository contains custom Checkov policies designed to enforce best practices around ephemeral resources and write-only attributes in Terraform configurations. These checks help identify opportunities to improve security and reduce state management complexity by preferring ephemeral data sources and write-only attributes where appropriate.

## Overview

The Checkov custom checks includes three main categories of checks:

1. **Ephemeral Creation Checks** - Identify resources that could be replaced with ephemeral data sources
2. **Ephemeral Retrieval Checks** - Detect data sources that should be marked as ephemeral
3. **Write-Only Attribute Checks** - Flag sensitive attributes that should be write-only

## Checks Included

* CKV2_EPH_CREATE - Prefer Ephemeral Resources for Creation
Identifies Terraform resources that create ephemeral data (like secrets, tokens, or temporary credentials) and suggests using ephemeral data sources instead. This helps reduce state file exposure and improves security posture.

* CKV2_EPH_RET - Prefer Ephemeral Resources for Retrieval  
Detects data sources that retrieve sensitive or temporary information and recommends marking them as ephemeral to prevent storage in state files.

* CKV2_EPH_WO - Prefer Write-Only Attributes
Flags sensitive resource attributes that should be configured as write-only to prevent them from being stored in or read from the Terraform state file.

## Usage

### Running All Custom Checks
You can also run the checks directly with Checkov:

```bash
checkov \
  --external-checks-dir ./checks \
  --directory ./tests \
  --framework terraform \
  --check CKV2_EPH_CREATE,CKV2_EPH_RET,CKV2_EPH_WO
```

### Running Individual Checks
To run specific checks, use the check IDs:

```bash
# Run only ephemeral creation checks
checkov --external-checks-dir ./checks --directory ./tests --check CKV2_EPH_CREATE

# Run only write-only attribute checks  
checkov --external-checks-dir ./checks --directory ./tests --check CKV2_EPH_WO
```

## Configuration

The checks are driven by data files in the `data/` directory:

### Main Configuration File
- **`ephemerality.json`** - Combined resource classifications (automatically generated)
  - Contains `ephemeral` array from generated schema analysis
  - Contains `resources` array from manual curation
  - Contains `write_only` object with resource-to-attribute mappings

### Source Files (Auto-Generated)
- **`ephemeral/gen_schema_ephemerals.json`** - Ephemeral resources discovered from Terraform provider schemas
- **`write-only/gen_write_only.json`** - Write-only attributes discovered from provider schemas

### Source Files (Manual)
- **`ephemeral/manual_resources.json`** - Manually curated ephemeral resources

## Automated Resource Generation

This repository includes an automated workflow that:

1. **Runs daily at 4:00 UTC** to check for new provider resources
2. **Analyzes Terraform provider schemas** to discover new ephemeral resources and write-only attributes
3. **Combines generated data** with manual configurations into `ephemerality.json`
4. **Creates pull requests** automatically when changes are detected
5. **Can be triggered manually** via GitHub Actions workflow dispatch

### Manual Workflow Trigger
You can manually trigger the generation workflow from the GitHub Actions tab or using the GitHub CLI:

## Requirements

- Checkov
- Terraform (for testing and generation)

## Usage

1. Clone this repository
2. Install Checkov: `pip install checkov`
3. Run the checks using Checkov with the either `--external-checks-dir`.

Or

1. Run the checks using Checkov with the flag `--external-checks-git`. Use the checks reference since the examples in this main branch might lead to checkov identifying them as part of your configuration.


## Contributing

When adding new checks or updating existing ones:

1. **For new ephemeral resources**: Add them to `data/ephemeral/manual_resources.json`
2. **For new write-only attributes**: The automated workflow will discover them, or add manually to the generated files
3. **Add test cases** in `tests/` directory
4. **Update documentation** as needed
5. **Test your changes** with the provided test suite

The `ephemerality.json` file is automatically regenerated, so don't edit it directly.

## Credits

This Checkov custom checks is inspired by and builds upon the work from [drewmullen/policy-library-ephemerality](https://github.com/drewmullen/policy-library-ephemerality). Special thanks to Drew  for the foundational concepts and approach to this.
