# Engine/requirements.py

import os
import subprocess
import sys
from .menu_logger import Logger

def check_tool(tool_name):
    """Check if a tool is installed and available in PATH."""
    try:
        # Use 'which' on Linux/macOS, 'where' on Windows
        if os.name == 'nt':  # Windows
            result = subprocess.run(['where', tool_name], 
                                  capture_output=True, text=True, timeout=10)
        else:  # Linux/macOS
            result = subprocess.run(['which', tool_name], 
                                  capture_output=True, text=True, timeout=10)
        
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def install_apt_package(package_name):
    """Install a package using apt (Debian/Ubuntu/Kali)."""
    try:
        Logger.info(f"Installing {package_name} via apt...")
        result = subprocess.run(['sudo', 'apt', 'install', '-y', package_name],
                              capture_output=True, text=True, timeout=300)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        Logger.error(f"Timeout installing {package_name}")
        return False

def install_go_tool(tool_url):
    """Install a Go-based tool."""
    try:
        Logger.info(f"Installing Go tool: {tool_url}")
        result = subprocess.run(['go', 'install', '-v', tool_url],
                              capture_output=True, text=True, timeout=600)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        Logger.error("Timeout installing Go tool")
        return False
    except FileNotFoundError:
        Logger.error("Go is not installed. Installing Go first...")
        if install_apt_package('golang-go'):
            return install_go_tool(tool_url)
        return False

def install_eyewitness():
    """Install EyeWitness tool from GitHub."""
    try:
        Logger.info("Installing EyeWitness...")
        # Clone repository
        clone_cmd = ['git', 'clone', 'https://github.com/FortyNorthSecurity/EyeWitness.git', '/tmp/EyeWitness']
        result = subprocess.run(clone_cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            return False
        
        # Run setup script
        setup_cmd = ['sudo', 'python3', '/tmp/EyeWitness/setup/setup.py']
        result = subprocess.run(setup_cmd, capture_output=True, text=True, timeout=300)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        Logger.error("Timeout installing EyeWitness")
        return False

def check_and_install_all():
    """Check all dependencies and install missing ones."""
    Logger.info("Checking system dependencies...")
    
    # Define all tools and their installation methods
    dependencies = {
        'whois': {'type': 'apt', 'package': 'whois'},
        'nmap': {'type': 'apt', 'package': 'nmap'},
        'subfinder': {'type': 'go', 'url': 'github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest'},
        'amass': {'type': 'go', 'url': 'github.com/owasp-amass/amass/v3/...@master'},
        'httpx': {'type': 'go', 'url': 'github.com/projectdiscovery/httpx/cmd/httpx@latest'},
        'EyeWitness': {'type': 'custom', 'install_func': install_eyewitness}
    }
    
    missing_tools = []
    
    # Check each tool
    for tool, info in dependencies.items():
        if check_tool(tool if tool != 'EyeWitness' else 'python3'):
            Logger.success(f"{tool} is already installed")
        else:
            Logger.error(f"{tool} not found")
            missing_tools.append((tool, info))
    
    # If no missing tools, return early
    if not missing_tools:
        Logger.success("All dependencies are installed!")
        return True
    
    # Ask user for installation
    Logger.warning(f"{len(missing_tools)} tools are missing.")
    choice = input("[?] Would you like to install missing dependencies? (y/n): ").lower().strip()
    
    if choice != 'y':
        Logger.warning("Some modules may not function without missing dependencies.")
        return False
    
    # Install missing tools
    for tool, info in missing_tools:
        Logger.info(f"Installing {tool}...")
        success = False
        
        if info['type'] == 'apt':
            success = install_apt_package(info['package'])
        elif info['type'] == 'go':
            success = install_go_tool(info['url'])
        elif info['type'] == 'custom':
            success = info['install_func']()
        
        if success:
            Logger.success(f"{tool} installed successfully")
        else:
            Logger.error(f"Failed to install {tool}")
    
    # Final verification
    all_installed = True
    for tool, _ in missing_tools:
        if not check_tool(tool if tool != 'EyeWitness' else 'python3'):
            Logger.error(f"{tool} is still not available after installation")
            all_installed = False
    
    if all_installed:
        Logger.success("All dependencies installed successfully!")
    else:
        Logger.warning("Some dependencies may not be fully functional")
    
    return all_installed

if __name__ == "__main__":
    # Test the dependency checker
    check_and_install_all()
