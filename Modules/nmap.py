# Nmap module execution
import subprocess
import os
import sys

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Engine.logger import info, error
from Engine.menu import nmap_submenu

def run(target, output_dir, report_enabled=False, scan_type=None):
    """Run the nmap tool on the target."""
    try:
        # If scan_type is not provided (e.g., from Run All), use default quick scan
        if scan_type is None:
            scan_type, nmap_report_enabled = nmap_submenu()
        else:
            # For Run All, use the provided scan_type and don't ask for report
            nmap_report_enabled = report_enabled
        
        # Determine input source: file or single target
        if target.startswith('@'):
            # File input - use -iL flag
            file_path = target[1:]  # Remove the @ symbol
            input_spec = f"-iL {file_path}"
        else:
            # Single target
            input_spec = target
        
        # Define commands based on scan type
        commands = {
            'quick': f"nmap {input_spec} -T4 --top-ports 1000 -sS -sV -O -sC -oN {output_dir}/Logs/nmap_top1000.txt",
            'full': f"nmap {input_spec} -T4 -p- -sS -sV -O -sC -oN {output_dir}/Logs/nmap_full.txt",
            'fast': f"nmap {input_spec} -T4 -A -sS -sV -O -sC -oN {output_dir}/Logs/nmap_fast.txt",
            'udp': f"nmap {input_spec} -T4 -sU --top-ports 100 -sV -O -sC -oN {output_dir}/Logs/nmap_udp.txt"
        }
        command = commands.get(scan_type, commands['quick'])
        
        info(f"Running: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            info(f"Nmap {scan_type} scan results saved.")
            
            # Handle report generation if requested
            if nmap_report_enabled:
                info("Nmap report generation would happen here")
            
            return True
        else:
            error(f"Nmap failed: {result.stderr}")
            return False
    except Exception as e:
        error(f"Error executing nmap: {e}")
        return False
