# HTTPX module execution (using httpx-toolkit)
import subprocess
import os
import sys

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Engine.logger import info, error

def run(target, output_dir):
    """Run the httpx-toolkit on the target."""
    try:
        merged_file = f"{output_dir}/Logs/merged_subs.txt"
        
        # httpx-toolkit command (Kali Linux package)
        command = f"cat {merged_file} | httpx-toolkit -silent -o {output_dir}/Logs/alive.txt"
        
        info(f"Running: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            info(f"HTTPX results saved to: {output_dir}/Logs/alive.txt")
            return True
        else:
            error(f"HTTPX failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        error("HTTPX timed out after 2 minutes. Skipping.")
        return False
    except Exception as e:
        error(f"Error executing httpx-toolkit: {e}")
        return False
