# Screenshot (Eyewitness) module execution
import subprocess
from Engine.logger import info, error

def run(target, output_dir):
    """Run the eyewitness tool on the target."""
    try:
        # This module requires the alive hosts list from HTTPX
        input_file = f"{output_dir}/Logs/alive.txt" # Placeholder
        command = f"eyewitness --web -f {input_file} -d {output_dir}/Screenshots/ --no-prompt"
        
        info(f"Running: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            info(f"Screenshots saved to: {output_dir}/Screenshots/")
            return True
        else:
            error(f"Eyewitness failed: {result.stderr}")
            return False
    except Exception as e:
        error(f"Error executing eyewitness: {e}")
        return False
