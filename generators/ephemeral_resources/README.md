# Generate List of Provider Ephemeral Resources

You can generate a list of ephemeral resources, as defined various providers.

```shell
terraform init
terraform providers schema -json | jq '{"ephemeral": [.provider_schemas | to_entries[] | .value.ephemeral_resource_schemas? | select(.) | keys[] ]}' > ../../data/ephemeral/gen_schema_ephemerals.json
```

## Generate list for write-only resources

```shell
terraform providers schema -json | jq '.provider_schemas | to_entries | map(.value.resource_schemas | to_entries | map(select(.value.block.attributes != null)) | map(select(.value.block.attributes | keys[] | test("^(?!has_).*_wo$"))) | map({key: .key, value: (.value.block.attributes | keys[] | select(test("^(?!has_).*_wo$")))})) | flatten | map({key: .key, value: .value}) | from_entries' > ../../data/gen_write_only.json
```

## Add new providers

The above code scrapes an arbitrary list of Terraform Providers for all published ephemeral resources. To add more providers to scrape from please:
1. update [here]()
1. run the commands from the top of this document
1. submit a PR
1. profit