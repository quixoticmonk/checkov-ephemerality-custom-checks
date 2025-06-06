import json
import os
import sys

# Import version checking utilities
utils_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "utils")
sys.path.insert(0, utils_dir)

try:
    from version_checker import (
        get_terraform_version_from_plan, 
        should_skip_check_for_version, 
        should_skip_ephemerality_check
    )
except ImportError:
    # Fallback implementations if version_checker is not available
    import re
    from packaging import version
    
    def get_terraform_version_from_plan(plan_dict):
        """Fallback implementation"""
        if not plan_dict:
            return None
        terraform_version = plan_dict.get("terraform_version")
        if terraform_version:
            return terraform_version
        format_version = plan_dict.get("format_version")
        if format_version:
            return format_version
        return None
    
    def should_skip_check_for_version(terraform_version, minimum_version="1.11.0"):
        """Fallback implementation"""
        if not terraform_version:
            return False
        clean_version = re.sub(r'[^0-9.]', '', terraform_version)
        try:
            return version.parse(clean_version) < version.parse(minimum_version)
        except (TypeError, ValueError):
            return False
    
    def should_skip_ephemerality_check(plan_dict=None):
        """Fallback implementation"""
        if plan_dict:
            plan_version = get_terraform_version_from_plan(plan_dict)
            if plan_version and should_skip_check_for_version(plan_version):
                return True
        return False


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


# Legacy function names for backward compatibility
def should_skip_check(terraform_version):
    """
    Legacy function - use should_skip_check_for_version instead.
    """
    return should_skip_check_for_version(terraform_version)
