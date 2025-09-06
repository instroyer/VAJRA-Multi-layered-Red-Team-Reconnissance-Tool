# Amass module execution
import subprocess
from Engine.logger import info, error

def run(target, output_dir):
    """Run the amass tool on the target."""
    try:
        log_file = f"{output_dir}/Logs/amass.txt"
        command = f"amass enum -d {target} -o {log_file}"
        
        info(f"Running: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            info(f"Amass results saved to: {log_file}")
            return True
        else:
            error(f"Amass failed: {result.stderr}")
            return False
    except Exception as e:
        error(f"Error executing amass: {e}")
        return False
