# VAJRA/Modules/nmap.py
# Nmap module execution, using the centralized submenu from Engine/menu.py

import subprocess
import os
import sys
from Engine.logger import info, error, success
from Engine.menu import nmap_submenu # <-- Correctly imports your submenu
from Engine.report import generate_report # <-- Import report generator

def _ensure_logs_dir(output_dir):
    """Ensures the Logs subdirectory exists."""
    logs_dir = os.path.join(output_dir, "Logs")
    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir

def run(target, output_dir):
    """Run the nmap tool on the target."""
    info("--- Starting module: Nmap ---")
    
    # Use the centralized submenu to get user choices
    scan_type, nmap_report_enabled = nmap_submenu()

    logs_dir = _ensure_logs_dir(output_dir)

    # Define commands and output paths based on the chosen scan_type
    out_paths = {
        'quick': (os.path.join(logs_dir, "nmap_top1000.txt"), os.path.join(logs_dir, "nmap_top1000.xml")),
        'full': (os.path.join(logs_dir, "nmap_full.txt"), os.path.join(logs_dir, "nmap_full.xml")),
        'fast': (os.path.join(logs_dir, "nmap_fastA.txt"), os.path.join(logs_dir, "nmap_fastA.xml")),
        'udp': (os.path.join(logs_dir, "nmap_udp.txt"), os.path.join(logs_dir, "nmap_udp.xml"))
    }
    
    commands = {
        'quick': ["nmap", target, "-T4", "--top-ports", "1000", "-sS", "-sV", "-O"],
        'full': ["nmap", target, "-T4", "-p-", "-sS", "-sV", "-O"],
        'fast': ["nmap", target, "-T4", "-A"],
        'udp': ["nmap", target, "-T4", "-sU", "--top-ports", "100"]
    }

    # Get the command and output files for the selected scan type
    command = commands.get(scan_type)
    out_n, out_x = out_paths.get(scan_type)
    
    # Add the output file flags to the command
    command.extend(["-oN", out_n, "-oX", out_x])

    try:
        info(f"Running: {' '.join(command)}")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        info(f"Nmap {scan_type} scan completed.")
        info(f"Output: {out_n}")
        
        # Trigger report generation if the user requested it
        if nmap_report_enabled:
            info("Generating HTML report...")
            # We pass "5" because that's the module choice for Nmap from the main menu
            if generate_report(target, output_dir, "5"):
                success("HTML report generation successful.")
            else:
                error("Failed to generate HTML report.")

    except FileNotFoundError:
        error("Nmap command not found. Please ensure Nmap is installed and in your system's PATH.")
    except subprocess.CalledProcessError as e:
        error(f"Nmap failed: {e.stderr.strip()}")
    except Exception as e:
        error(f"An error occurred while executing nmap: {e}")

    success("Module Nmap completed successfully.")
