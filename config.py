# VAJRA Configuration Settings
# API keys, tool paths, default parameters, output preferences

import os

# --- Tool Paths (Ensure these are in your system's PATH or update these paths) ---
TOOL_PATHS = {
    'whois': 'whois',           # Default system whois
    'subfinder': 'subfinder',
    'amass': 'amass',
    'httpx': 'httpx',
    'nmap': 'nmap',
    'eyewitness': 'eyewitness', # Assuming Python version
}

# --- API Keys (Add your keys here) ---
API_KEYS = {
    'virustotal': 'YOUR_VIRUSTOTAL_API_KEY',
    'shodan': 'YOUR_SHODAN_API_KEY',
    # ... other API keys
}

# --- Default Parameters ---
DEFAULT_NMAP_SCAN = 'quick'  # 'quick', 'full', 'fast', 'udp'

# --- Output & Report Preferences ---
REPORT_FORMAT = 'html'  # 'html', 'pdf'
VERBOSE_LOGGING = False
