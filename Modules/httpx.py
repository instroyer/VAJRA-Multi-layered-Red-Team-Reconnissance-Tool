# Httpx module execution
import subprocess
from Engine.logger import info, error

def run(target, output_dir):
    """Run the httpx tool on the target."""
    try:
        # This module requires the merged subdomain list from Subfinder+Amass
        # For now, it runs on the target itself. Logic to merge files needed later.
        input_file = f"{output_dir}/Logs/merged_subs.txt" # Placeholder
        alive_file = f"{output_dir}/Logs/alive.txt"
        # TODO: Implement logic to create merged_subs.txt if running in sequence '0'
        command = f"httpx -l {input_file} -silent -o {alive_file}"
        
        info(f"Running: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            info(f"HTTPX results saved to: {alive_file}")
            return True
        else:
            error(f"HTTPX failed: {result.stderr}")
            return False
    except Exception as e:
        error(f"Error executing httpx: {e}")
        return False
