from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories
import os
import sys
import importlib.util

# Add the current directory to the path to import data_loader
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Try to import data_loader functions with error handling
try:
    from data_loader import load_ephemerality_data, get_terraform_version_from_plan, should_skip_check
except ImportError:
    # Fallback: load the module directly
    spec = importlib.util.spec_from_file_location("data_loader", os.path.join(current_dir, "data_loader.py"))
    data_loader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(data_loader)
    load_ephemerality_data = data_loader.load_ephemerality_data
    get_terraform_version_from_plan = data_loader.get_terraform_version_from_plan
    should_skip_check = data_loader.should_skip_check

class PreferEphemeralCreates(BaseResourceCheck):
    def __init__(self):
        name = "Prefer Ephemeral Resources for Creation"
        id = "CKV2_EPH_CREATE"
        supported_resources = ["*"]
        categories = [CheckCategories.SECRETS]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)
        self.ephemerality_data = load_ephemerality_data()
        
    def scan_resource_conf(self, conf, resource_type=None):
        """
        Checks if resources that create secret values are using ephemeral alternatives.
        
        :param conf: The resource configuration
        :param resource_type: The resource type (passed by Checkov)
        :return: CheckResult.PASSED if the resource is not in the resources list or if Terraform version < 1.11,
                 CheckResult.FAILED otherwise
        """
        # Try to get Terraform version from plan if available
        terraform_version = None
        try:
            # This is a best effort attempt to get the Terraform version
            # It may not always be available depending on how Checkov is run
            runner_filter = getattr(self, 'runner_filter', None)
            if runner_filter and hasattr(runner_filter, 'tf_plan_dict'):
                terraform_version = get_terraform_version_from_plan(runner_filter.tf_plan_dict)
        except Exception:
            pass
            
        # Skip check for Terraform versions < 1.11
        if terraform_version and should_skip_check(terraform_version):
            return CheckResult.PASSED
            
        # Get resource type from parameter or entity_type
        if resource_type:
            current_resource_type = resource_type
        else:
            current_resource_type = getattr(self, 'entity_type', None)
            
        if not current_resource_type:
            return CheckResult.PASSED
        
        # Check if the resource has an ephemeral alternative
        # FAIL if using a regular resource that has an ephemeral alternative available
        ephemeral_alternatives = self.ephemerality_data.get("resources", [])
        
        # If this resource type has an ephemeral alternative, FAIL
        if current_resource_type in ephemeral_alternatives:
            return CheckResult.FAILED
        
        return CheckResult.PASSED


check = PreferEphemeralCreates()
