# Whois module execution
import subprocess
import os
import sys

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Engine.logger import info, error

def run(target, output_dir):
    """Run the whois tool on the target."""
    try:
        # Construct the command
        log_file = f"{output_dir}/Logs/whois.txt"
        command = f"whois {target} > {log_file}"
        
        info(f"Running: {command}")
        # Execute the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            info(f"Whois results saved to: {log_file}")
            return True
        else:
            error(f"Whois failed: {result.stderr}")
            return False
    except Exception as e:
        error(f"Error executing whois: {e}")
        return False
