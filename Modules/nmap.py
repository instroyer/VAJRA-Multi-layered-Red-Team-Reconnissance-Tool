# VAJRA/Modules/nmap.py
# Nmap module execution
import subprocess
import os
import sys

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Engine.logger import info, error
from Engine.menu import nmap_submenu

def _ensure_logs_dir(output_dir):
    logs_dir = os.path.join(output_dir, "Logs")
    try:
        os.makedirs(logs_dir, exist_ok=True)
    except Exception as e:
        error(f"Could not ensure Logs directory: {e}")
    return logs_dir

def run(target, output_dir, report_enabled=False, scan_type=None):
    """Run the nmap tool on the target."""
    try:
        # If scan_type is provided (from Run All), use it without asking
        if scan_type is not None:
            nmap_report_enabled = report_enabled
            info(f"Using {scan_type} scan (Run All mode)")
        else:
            # Otherwise, ask user via submenu
            scan_type, nmap_report_enabled = nmap_submenu()

        # Ensure Logs directory exists
        logs_dir = _ensure_logs_dir(output_dir)

        # Determine input source: file or single target
        if str(target).startswith('@'):
            file_path = str(target)[1:]  # Remove the @ symbol
            input_spec = f"-iL {file_path}"
        else:
            input_spec = str(target)

        # Define output file paths
        out_paths = {
            'quick': (
                os.path.join(logs_dir, "nmap_top1000.txt"),
                os.path.join(logs_dir, "nmap_top1000.xml")
            ),
            'full': (
                os.path.join(logs_dir, "nmap_full.txt"),
                os.path.join(logs_dir, "nmap_full.xml")
            ),
            'fast': (
                os.path.join(logs_dir, "nmap_fast.txt"),
                os.path.join(logs_dir, "nmap_fast.xml")
            ),
            'udp': (
                os.path.join(logs_dir, "nmap_udp.txt"),
                os.path.join(logs_dir, "nmap_udp.xml")
            )
        }

        out_n, out_x = out_paths.get(scan_type, out_paths['quick'])

        # Define commands based on scan type
        commands = {
            'quick': f"nmap {input_spec} -T4 --top-ports 1000 -sS -sV -O -oN {out_n} -oX {out_x}",
            'full': f"nmap {input_spec} -T4 -p- -sS -sV -O -oN {out_n} -oX {out_x}",
            'fast': f"nmap {input_spec} -T4 -A -sS -sV -O -oN {out_n} -oX {out_x}",
            'udp': f"nmap {input_spec} -T4 -sU --top-ports 100 -sV -O -oN {out_n} -oX {out_x}"
        }

        command = commands.get(scan_type, commands['quick'])
        info(f"Running: {command}")
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            info(f"Nmap {scan_type} scan completed.")
            info(f"Output: {out_n}")
            return True
        else:
            error(f"Nmap failed: {result.stderr}")
            return False

    except Exception as e:
        error(f"Error executing nmap: {e}")
        return False
