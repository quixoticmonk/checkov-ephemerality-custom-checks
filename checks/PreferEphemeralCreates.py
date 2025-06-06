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
    from data_loader import load_ephemerality_data, should_skip_ephemerality_check
except ImportError:
    # Fallback: load the module directly
    spec = importlib.util.spec_from_file_location("data_loader", os.path.join(current_dir, "data_loader.py"))
    data_loader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(data_loader)
    load_ephemerality_data = data_loader.load_ephemerality_data
    should_skip_ephemerality_check = data_loader.should_skip_ephemerality_check

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
        :return: CheckResult.PASSED if the resource is not in the resources list or if Terraform version < 1.11.0,
                 CheckResult.FAILED otherwise
        """
        # Check if we should skip this check due to Terraform version < 1.11.0
        try:
            # Try to get plan from runner_filter if available
            plan_dict = None
            runner_filter = getattr(self, 'runner_filter', None)
            if runner_filter and hasattr(runner_filter, 'tf_plan_dict'):
                plan_dict = runner_filter.tf_plan_dict
            
            # Skip check for Terraform versions < 1.11.0
            if should_skip_ephemerality_check(plan_dict):
                return CheckResult.PASSED
        except Exception:
            # If version checking fails, continue with the check
            pass
            
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
