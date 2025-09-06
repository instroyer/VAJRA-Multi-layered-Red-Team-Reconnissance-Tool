# File and directory operations for VAJRA
import os
from datetime import datetime
from .logger import info, error

def create_target_dirs(base_results_dir, target, is_file_input=False, file_name=None):
    """
    Creates the organized directory structure for a target.
    Results/Target_YYYYMMDD_HHMMSS/ or Results/Filename/Target_YYYYMMDD_HHMMSS/
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if is_file_input and file_name:
            # For file inputs: Results/Filename/Target_YYYYMMDD_HHMMSS/
            base_dir = os.path.join(base_results_dir, file_name, f"{target}_{timestamp}")
        else:
            # For single targets: Results/Target_YYYYMMDD_HHMMSS/
            base_dir = os.path.join(base_results_dir, f"{target}_{timestamp}")
        
        dirs_to_create = [
            base_dir,
            os.path.join(base_dir, "Logs"),
            os.path.join(base_dir, "Reports"),
            os.path.join(base_dir, "Screenshots"),
            os.path.join(base_dir, "JSON")
        ]
        
        for directory in dirs_to_create:
            os.makedirs(directory, exist_ok=True)
        
        return base_dir
    except OSError as e:
        error(f"Could not create directories: {e}")
        return None
