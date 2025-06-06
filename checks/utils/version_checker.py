import os
import re
import subprocess
import json
from packaging import version


def get_terraform_version():
    """
    Get Terraform version using multiple methods in order of preference:
    1. From terraform binary directly
    2. From environment variable TF_VERSION
    3. From .terraform-version file
    4. From terraform plan if available
    
    :return: Terraform version as string, or None if not found
    """
    # Method 1: Try to get version from terraform binary
    try:
        result = subprocess.run(['terraform', 'version', '-json'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_data = json.loads(result.stdout)
            terraform_version = version_data.get('terraform_version')
            if terraform_version:
                return terraform_version
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, 
            json.JSONDecodeError, FileNotFoundError):
        pass
    
    # Method 2: Try to get version from terraform binary (text output)
    try:
        result = subprocess.run(['terraform', 'version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            # Parse output like "Terraform v1.11.0"
            match = re.search(r'Terraform v?(\d+\.\d+\.\d+)', result.stdout)
            if match:
                return match.group(1)
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Method 3: Check environment variable
    env_version = os.environ.get('TF_VERSION')
    if env_version:
        return clean_version_string(env_version)
    
    # Method 4: Check .terraform-version file
    terraform_version_file = '.terraform-version'
    if os.path.exists(terraform_version_file):
        try:
            with open(terraform_version_file, 'r') as f:
                file_version = f.read().strip()
                if file_version:
                    return clean_version_string(file_version)
        except (IOError, OSError):
            pass
    
    # Method 5: Check for .terraform-version in parent directories
    current_dir = os.getcwd()
    while current_dir != os.path.dirname(current_dir):  # Stop at root
        version_file = os.path.join(current_dir, '.terraform-version')
        if os.path.exists(version_file):
            try:
                with open(version_file, 'r') as f:
                    file_version = f.read().strip()
                    if file_version:
                        return clean_version_string(file_version)
            except (IOError, OSError):
                pass
        current_dir = os.path.dirname(current_dir)
    
    return None


def get_terraform_version_from_plan(plan_dict):
    """
    Extract Terraform version from plan dictionary.
    
    :param plan_dict: Terraform plan as dictionary
    :return: Terraform version as string, or None if not found
    """
    if not plan_dict:
        return None
    
    # Try to get version from terraform_version field
    terraform_version = plan_dict.get("terraform_version")
    if terraform_version:
        return clean_version_string(terraform_version)
    
    # Try to get version from format_version field
    format_version = plan_dict.get("format_version")
    if format_version:
        return clean_version_string(format_version)
    
    return None


def clean_version_string(version_string):
    """
    Clean up version string to extract just the version number.
    
    :param version_string: Raw version string
    :return: Cleaned version string
    """
    if not version_string:
        return None
    
    # Remove 'v' prefix and any non-numeric/dot characters at the end
    clean_version = re.sub(r'^v?', '', version_string)
    clean_version = re.match(r'(\d+\.\d+(?:\.\d+)?)', clean_version)
    
    if clean_version:
        return clean_version.group(1)
    
    return None


def should_skip_check_for_version(terraform_version, minimum_version="1.11.0"):
    """
    Determine if check should be skipped based on Terraform version.
    Skip for versions below the minimum version.
    
    :param terraform_version: Terraform version as string
    :param minimum_version: Minimum required version (default: 1.11.0)
    :return: True if check should be skipped, False otherwise
    """
    if not terraform_version:
        # If we can't determine the version, don't skip the check
        # This ensures we don't accidentally skip checks when version detection fails
        return False
    
    clean_tf_version = clean_version_string(terraform_version)
    if not clean_tf_version:
        return False
    
    try:
        return version.parse(clean_tf_version) < version.parse(minimum_version)
    except (TypeError, ValueError):
        # If version parsing fails, don't skip the check
        return False


def should_skip_ephemerality_check(plan_dict=None):
    """
    Determine if ephemerality checks should be skipped.
    Checks for Terraform version < 1.11.0 using multiple detection methods.
    
    :param plan_dict: Optional Terraform plan dictionary
    :return: True if check should be skipped, False otherwise
    """
    # Try to get version from plan first if available
    if plan_dict:
        plan_version = get_terraform_version_from_plan(plan_dict)
        if plan_version and should_skip_check_for_version(plan_version):
            return True
    
    # Try to get version from system
    system_version = get_terraform_version()
    if system_version and should_skip_check_for_version(system_version):
        return True
    
    # If we can't determine the version, don't skip
    return False
