# HTTPX module execution (using httpx-toolkit)
import subprocess
import os
import sys

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Engine.logger import info, error

def extract_urls_from_json(json_file, output_file):
    """Extract clean URLs from httpx JSON output using jq and sed"""
    try:
        # Extract URLs and clean them (remove protocol prefixes, keep only hostname)
        # This makes the output compatible with Nmap and other tools
        command = f"jq -r '.url' {json_file} | sed -E 's#(https?://)?([^:/]+).*#\\2#' | sort -u > {output_file}"
        info(f"Extracting URLs: {command}")
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Count lines to show how many URLs were extracted
            with open(output_file, 'r') as f:
                url_count = len(f.readlines())
            info(f"Extracted {url_count} unique hostnames to: {output_file}")
            return True
        else:
            error(f"URL extraction failed: {result.stderr}")
            return False
            
    except Exception as e:
        error(f"Error extracting URLs from JSON: {e}")
        return False

def run(target, output_dir):
    """Run the httpx-toolkit on the target and extract clean hostnames"""
    try:
        merged_file = f"{output_dir}/Logs/merged_subs.txt"
        json_output = f"{output_dir}/Logs/alive.json"
        txt_output = f"{output_dir}/Logs/alive.txt"
        
        # Check if we have subdomains to process
        if not os.path.exists(merged_file) or os.path.getsize(merged_file) == 0:
            error("No subdomains found to process. Skipping HTTPX.")
            return False

        # httpx-toolkit command with JSON output
        command = f"cat {merged_file} | httpx-toolkit -json -o {json_output}"
        info(f"Running: {command}")
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)

        if result.returncode == 0:
            info(f"HTTPX JSON results saved to: {json_output}")
            
            # Extract clean hostnames from JSON to create Nmap-compatible alive.txt
            if extract_urls_from_json(json_output, txt_output):
                info("HTTPX completed successfully. Both JSON and clean hostname formats available.")
                
                # Show sample of extracted hostnames for user confirmation
                try:
                    with open(txt_output, 'r') as f:
                        hosts = f.readlines()[:5]  # Show first 5 hosts
                    if hosts:
                        info(f"Sample hosts extracted: {', '.join([h.strip() for h in hosts])}{'...' if len(hosts) == 5 else ''}")
                except:
                    pass
                    
                return True
            else:
                error("HTTPX succeeded but hostname extraction failed.")
                return False
        else:
            error(f"HTTPX failed: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        error("HTTPX timed out after 2 minutes. Skipping.")
        return False
    except Exception as e:
        error(f"Error executing httpx-toolkit: {e}")
        return False
