# Engine/finaljson.py
# WHOIS data extraction and JSON creation utility

import json
import os
import re
from datetime import datetime
from .logger import info, warning, error

def extract_whois_info(whois_file_path):
    """
    Extract structured information from whois.txt file
    Returns a dictionary with parsed whois data
    """
    whois_data = {
        "domain_name": "",
        "registrar": "",
        "creation_date": "",
        "updated_date": "",
        "expiry_date": "",
        "registrant": {
            "name": "",
            "organization": "",
            "email": ""
        },
        "contacts": {
            "admin": {},
            "tech": {}
        },
        "name_servers": [],
        "dnssec": "",
        "raw_data": ""
    }
    
    try:
        with open(whois_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            raw_content = f.read()
            whois_data['raw_data'] = raw_content
            
            lines = raw_content.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # Domain Name
                if re.match(r'^(Domain Name|Domain):', line, re.IGNORECASE):
                    whois_data['domain_name'] = re.split(r':\s*', line, 1)[1].strip()
                
                # Registrar
                elif re.match(r'^(Registrar|Registrar Name):', line, re.IGNORECASE):
                    whois_data['registrar'] = re.split(r':\s*', line, 1)[1].strip()
                
                # Creation Date
                elif re.match(r'^(Creation Date|Created On|Registered on):', line, re.IGNORECASE):
                    whois_data['creation_date'] = re.split(r':\s*', line, 1)[1].strip()
                
                # Updated Date
                elif re.match(r'^(Updated Date|Last Updated|Modified Date):', line, re.IGNORECASE):
                    whois_data['updated_date'] = re.split(r':\s*', line, 1)[1].strip()
                
                # Expiry Date
                elif re.match(r'^(Expiry Date|Registry Expiry Date|Expiration Date):', line, re.IGNORECASE):
                    whois_data['expiry_date'] = re.split(r':\s*', line, 1)[1].strip()
                
                # Registrant Information
                elif re.match(r'^(Registrant Name|Registrant):', line, re.IGNORECASE):
                    whois_data['registrant']['name'] = re.split(r':\s*', line, 1)[1].strip()
                elif re.match(r'^(Registrant Organization):', line, re.IGNORECASE):
                    whois_data['registrant']['organization'] = re.split(r':\s*', line, 1)[1].strip()
                elif re.match(r'^(Registrant Email):', line, re.IGNORECASE):
                    whois_data['registrant']['email'] = re.split(r':\s*', line, 1)[1].strip()
                
                # Name Servers
                elif re.match(r'^(Name Server|Name Servers|NS):', line, re.IGNORECASE):
                    ns = re.split(r':\s*', line, 1)[1].strip()
                    if ns and ns not in whois_data['name_servers']:
                        whois_data['name_servers'].append(ns)
                
                # DNSSEC
                elif re.match(r'^(DNSSEC|dnssec):', line, re.IGNORECASE):
                    whois_data['dnssec'] = re.split(r':\s*', line, 1)[1].strip()
        
        # Additional parsing for multi-line patterns
        raw_lower = raw_content.lower()
        
        # Extract name servers (multi-line pattern)
        ns_match = re.search(r'name server[s]?:\s*((?:\s*[a-z0-9.-]+\s*)+)', raw_content, re.IGNORECASE | re.MULTILINE)
        if ns_match:
            ns_list = re.findall(r'[a-z0-9.-]+', ns_match.group(1), re.IGNORECASE)
            whois_data['name_servers'].extend([ns.strip() for ns in ns_list if ns.strip()])
        
        # Remove duplicates from name servers
        whois_data['name_servers'] = list(set(whois_data['name_servers']))
        
        return whois_data
        
    except Exception as e:
        error(f"Error parsing whois file: {e}")
        return None

def create_final_json(target_dir, module_choices):
    """
    Create final.json from whois data and other module outputs
    This function is called after module execution completes
    """
    try:
        whois_file = f"{target_dir}/Logs/whois.txt"
        json_output = f"{target_dir}/JSON/final.json"
        
        # Check if whois module was run (choices include 1 or 0 for all)
        whois_was_run = '1' in module_choices or module_choices == '0'
        
        if not whois_was_run:
            info("WHOIS module not selected, skipping final.json creation")
            return False
        
        if not os.path.exists(whois_file) or os.path.getsize(whois_file) == 0:
            warning("WHOIS file is empty or doesn't exist, skipping final.json creation")
            return False
        
        info("Extracting WHOIS information for final.json...")
        
        # Extract whois data
        whois_data = extract_whois_info(whois_file)
        if not whois_data:
            error("Failed to extract WHOIS information")
            return False
        
        # Create base structure for final.json
        final_data = {
            "target_information": {
                "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "modules_executed": module_choices if module_choices != '0' else "all"
            },
            "whois": whois_data,
            "subdomains": {
                "subfinder": [],
                "amass": [],
                "merged": [],
                "alive": []
            },
            "ports": {},
            "screenshots": []
        }
        
        # Try to add subdomain information if available
        try:
            # Subfinder results
            subfinder_file = f"{target_dir}/Logs/subfinder.txt"
            if os.path.exists(subfinder_file):
                with open(subfinder_file, 'r') as f:
                    final_data['subdomains']['subfinder'] = [line.strip() for line in f if line.strip()]
            
            # Amass results
            amass_file = f"{target_dir}/Logs/amass.txt"
            if os.path.exists(amass_file):
                with open(amass_file, 'r') as f:
                    final_data['subdomains']['amass'] = [line.strip() for line in f if line.strip()]
            
            # Merged results
            merged_file = f"{target_dir}/Logs/merged_subs.txt"
            if os.path.exists(merged_file):
                with open(merged_file, 'r') as f:
                    final_data['subdomains']['merged'] = [line.strip() for line in f if line.strip()]
            
            # Alive results
            alive_file = f"{target_dir}/Logs/alive.txt"
            if os.path.exists(alive_file):
                with open(alive_file, 'r') as f:
                    final_data['subdomains']['alive'] = [line.strip() for line in f if line.strip()]
                    
        except Exception as e:
            warning(f"Could not add subdomain information: {e}")
        
        # Save to JSON file
        with open(json_output, 'w') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)
        
        info(f"Final JSON created: {json_output}")
        return True
        
    except Exception as e:
        error(f"Error creating final.json: {e}")
        return False
