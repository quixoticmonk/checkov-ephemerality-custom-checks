from checkov.terraform.checks.data.base_check import BaseDataCheck
from checkov.common.models.enums import CheckResult, CheckCategories
import os
import sys
import importlib.util

# Import data_loader functions using importlib
current_dir = os.path.dirname(os.path.abspath(__file__))
data_loader_path = os.path.join(current_dir, 'data_loader.py')

spec = importlib.util.spec_from_file_location("data_loader", data_loader_path)
data_loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data_loader)

load_ephemerality_data = data_loader.load_ephemerality_data
should_skip_ephemerality_check = data_loader.should_skip_ephemerality_check

class PreferEphemeralRetrieves(BaseDataCheck):
    def __init__(self):
        name = "Prefer Ephemeral Resources for Data Retrieval"
        id = "CKV2_EPH_RET"
        supported_data = ["*"]
        categories = [CheckCategories.SECRETS]
        super().__init__(name=name, id=id, categories=categories, supported_data=supported_data)
        self.ephemerality_data = load_ephemerality_data()
        
    def scan_data_conf(self, conf, data_type=None):
        """
        Checks if data sources that retrieve secret values are using ephemeral alternatives.
        
        :param conf: The data source configuration
        :param data_type: The data source type (passed by Checkov)
        :return: CheckResult.PASSED if the data source is not in the ephemeral list or if Terraform version < 1.11.0,
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
            
        # Get data type from parameter or entity_type
        if data_type:
            current_data_type = data_type
        else:
            current_data_type = getattr(self, 'entity_type', None)
            
        if not current_data_type:
            return CheckResult.PASSED
        
        # Check if the data source has an ephemeral alternative
        # FAIL if using a data source that matches an available ephemeral resource name
        ephemeral_list = self.ephemerality_data.get("ephemeral", [])
        
        if current_data_type in ephemeral_list:
            return CheckResult.FAILED
        
        return CheckResult.PASSED


check = PreferEphemeralRetrieves()
