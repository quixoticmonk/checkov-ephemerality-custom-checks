#!/bin/bash

# Script to run only the custom ephemerality checks

echo "Running custom ephemerality checks..."

# Run only custom checks
checkov \
  --external-checks-dir ./checks \
  --directory ./tests \
  --framework terraform \
  --check CKV2_EPH_CREATE,CKV2_EPH_RET,CKV2_EPH_WO \
  "$@"
