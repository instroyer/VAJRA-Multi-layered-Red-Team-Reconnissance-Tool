# Dependency checking utility
import subprocess
import sys
from .logger import info, success, warning, error

# List of required tools
REQUIRED_TOOLS = {
    'whois': 'whois',
    'dig': 'dig',
    'subfinder': 'subfinder',
    'amass': 'amass',
    'httpx': 'httpx-toolkit',
    'nmap': 'nmap',
    'eyewitness': 'eyewitness',
    'jq': 'jq'  # Added for JSON processing in HTTPX module
}

def check_tool_installed(tool_name):
    """Check if a specific tool is installed and available in PATH."""
    try:
        result = subprocess.run(['which', tool_name], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False

def check_dependencies(silent=False):
    """
    Check if all required tools are installed.
    If silent=True, only return the missing tools without printing status.
    """
    missing_tools = []

    for tool_key, tool_name in REQUIRED_TOOLS.items():
        if check_tool_installed(tool_name):
            if not silent:
                success(f"{tool_name} found")
        else:
            if not silent:
                error(f"{tool_name} not found")
            missing_tools.append(tool_name)

    if not silent:
        if not missing_tools:
            success("All dependencies are satisfied!")
        else:
            warning(f"Missing tools: {', '.join(missing_tools)}")

    return missing_tools

def install_dependencies(missing_tools):
    """Offer to install missing dependencies."""
    if not missing_tools:
        return True

    warning(f"\nThe following tools are missing: {', '.join(missing_tools)}")

    try:
        choice = input("Do you want to install them? (y/n) > ").strip().lower()
        if choice != 'y':
            error("Cannot proceed without required tools. Exiting.")
            return False

        info("Installing missing tools...")

        # Try to install based on package manager
        package_managers = ['apt', 'pacman', 'dnf', 'yum']
        installed_successfully = []
        failed_to_install = []

        for pm in package_managers:
            if check_tool_installed(pm):
                info(f"Using {pm} package manager...")

                for tool in missing_tools:
                    # Special handling for different package names
                    package_name = tool
                    
                    if tool == 'dig':
                        if pm == 'apt':
                            package_name = 'dnsutils'
                        elif pm in ['pacman', 'dnf', 'yum']:
                            package_name = 'bind-utils'
                    
                    # Handle package name variations
                    if tool == 'httpx-toolkit' and pm == 'apt':
                        package_name = 'httpx-toolkit'
                    elif tool == 'httpx-toolkit' and pm in ['pacman', 'dnf', 'yum']:
                        package_name = 'httpx'  # May have different name in other distros
                    
                    if tool == 'jq':
                        package_name = 'jq'  # jq is consistent across package managers

                    # Build installation command based on package manager
                    if pm == 'apt':
                        command = f"sudo apt update && sudo apt install -y {package_name}"
                    elif pm == 'pacman':
                        command = f"sudo pacman -Syu --noconfirm {package_name}"
                    elif pm in ['dnf', 'yum']:
                        command = f"sudo {pm} install -y {package_name}"
                    else:
                        continue

                    info(f"Installing {tool} ({package_name})...")
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)

                    if result.returncode == 0:
                        success(f"{tool} installed successfully!")
                        installed_successfully.append(tool)
                    else:
                        error(f"Failed to install {tool}")
                        failed_to_install.append(tool)

                break  # Stop after finding the first available package manager

        # Update missing tools list
        still_missing = [tool for tool in missing_tools if tool not in installed_successfully]

        if still_missing:
            error(f"Could not install: {', '.join(still_missing)}")
            info("Please install these tools manually.")
            return False
        else:
            success("All tools installed successfully!")
            return True

    except KeyboardInterrupt:
        info("\nInstallation cancelled.")
        return False
