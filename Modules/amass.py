# Amass module execution
import subprocess
import os
import sys

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Engine.logger import info, error

def run(target, output_dir):
    """Run the amass tool on the target."""
    try:
        # Use different Amass commands to handle resolver issues
        commands_to_try = [
            f"amass enum -d {target} -o {output_dir}/Logs/amass.txt",
            f"amass enum -d {target} -r 8.8.8.8,1.1.1.1 -o {output_dir}/Logs/amass.txt",  # Specify resolvers
            f"amass enum -d {target} -r 8.8.8.8 -o {output_dir}/Logs/amass.txt",  # Single resolver
            f"amass enum -d {target} -config /etc/amass/config.ini -o {output_dir}/Logs/amass.txt"  # Use config
        ]
        
        for command in commands_to_try:
            info(f"Trying: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                info(f"Amass results saved to: {output_dir}/Logs/amass.txt")
                return True
            else:
                error(f"Amass attempt failed: {result.stderr}")
                continue
                
        error("All Amass attempts failed. Skipping Amass.")
        return False
        
    except subprocess.TimeoutExpired:
        error("Amass timed out after 5 minutes. Skipping.")
        return False
    except Exception as e:
        error(f"Error executing amass: {e}")
        return False
