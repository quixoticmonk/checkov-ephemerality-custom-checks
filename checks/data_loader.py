import json
import os
import re
from packaging import version

def load_ephemerality_data():
    """
    Load ephemerality data from the ephemerality.json file in the data directory.
    
    :return: Dictionary containing ephemerality data
    """
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    data_file = os.path.join(data_dir, "ephemerality.json")
    
    # Initialize data structure with defaults
    ephemerality_data = {
        "ephemeral": [],
        "resources": [],
        "write_only": {}
    }
    
    # Load data from ephemerality.json
    try:
        with open(data_file, "r") as f:
            loaded_data = json.load(f)
            # Update our data structure with loaded data
            for key in ephemerality_data:
                if key in loaded_data:
                    ephemerality_data[key] = loaded_data[key]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading ephemerality data: {e}")
    
    return ephemerality_data

def get_terraform_version_from_plan(plan_dict):
    """
    Extract Terraform version from plan.
    
    :param plan_dict: Terraform plan as dictionary
    :return: Terraform version as string, or None if not found
    """
    if not plan_dict:
        return None
    
    # Try to get version from terraform_version field
    terraform_version = plan_dict.get("terraform_version")
    if terraform_version:
        return terraform_version
    
    # Try to get version from format_version field (might be in format like "1.1")
    format_version = plan_dict.get("format_version")
    if format_version:
        return format_version
    
    return None

def should_skip_check(terraform_version):
    """
    Determine if check should be skipped based on Terraform version.
    Skip for versions < 1.11 as write-only was added in 1.11.
    
    :param terraform_version: Terraform version as string
    :return: True if check should be skipped, False otherwise
    """
    if not terraform_version:
        return False
    
    # Clean up version string (remove any non-numeric/dot characters)
    clean_version = re.sub(r'[^0-9.]', '', terraform_version)
    
    try:
        return version.parse(clean_version) < version.parse("1.11")
    except (TypeError, ValueError):
        # If version parsing fails, don't skip the check
        return False
