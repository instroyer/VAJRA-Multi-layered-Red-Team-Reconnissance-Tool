# KESTREL/Modules/dig.py
# Description: Performs DNS reconnaissance using dig (A, MX, NS, TXT, SOA).

import subprocess
import os
import shutil
import json
from Engine.logger import info, success, error, warning

def check_dig():
    """Check if dig is installed."""
    return shutil.which("dig") is not None

def parse_dig_output(raw_output):
    """
    Parses raw dig output into a structured dictionary.
    """
    records = {
        'A': [],
        'AAAA': [],
        'MX': [],
        'NS': [],
        'TXT': [],
        'SOA': []
    }
    
    for line in raw_output.splitlines():
        line = line.strip()
        if not line or line.startswith(';'):
            continue
            
        parts = line.split()
        if len(parts) < 4:
            continue
            
        try:
            # Find the 'IN' class and look at the next field
            if 'IN' in parts:
                idx = parts.index('IN')
                if idx + 1 < len(parts):
                    rtype = parts[idx + 1]
                    rdata = " ".join(parts[idx + 2:])
                    
                    if rtype in records:
                        records[rtype].append(rdata)
        except Exception:
            pass

    return records

def run(target, output_dir):
    """Run dig queries against the target."""
    
    info(f"--- Executing module: Dig (DNS Recon) ---")

    if not check_dig():
        error("Dig is not installed or not found in PATH.")
        return False

    dig_log = os.path.join(output_dir, "Logs", "dig.txt")
    json_output = os.path.join(output_dir, "Logs", "dig.json")

    # Ensure Logs directory exists
    os.makedirs(os.path.dirname(dig_log), exist_ok=True)

    try:
        # Perform queries for multiple record types
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
        full_output = ""
        
        for rtype in record_types:
            cmd = ["dig", target, rtype, "+noall", "+answer"]
            info(f"Querying {rtype} records...")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                output = result.stdout
                if output.strip():
                     full_output += f";; TYPE: {rtype}\n{output}\n"
                else:
                     full_output += f";; TYPE: {rtype}\n; No records found\n\n"
            else:
                error(f"Dig failed for {rtype}: {result.stderr}")

        # Save raw output
        with open(dig_log, "w") as f:
            f.write(full_output)
        
        info(f"Dig raw output saved to: {dig_log}")

        # Parse and save JSON
        structured_data = parse_dig_output(full_output)
        with open(json_output, "w") as f:
            json.dump(structured_data, f, indent=4)
            
        success(f"Dig analysis completed. Data saved to: {json_output}")
        info("--- Module execution completed ---")
        return True

    except Exception as e:
        error(f"An error occurred during Dig execution: {e}")
        return False
