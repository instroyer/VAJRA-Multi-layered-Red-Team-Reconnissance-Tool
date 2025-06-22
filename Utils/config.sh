#!/bin/bash

# ===================================================
# 🔧 VAJRA Framework — Global Configuration File
# Author: YJ (VAJRA Framework)
# Description: Centralized config for timeouts, concurrency,
#              tool settings, logging, and feature toggles
# ===================================================

# === Timeout Settings ===
DEFAULT_TIMEOUT=20                     # General timeout (in seconds) for tools like EyeWitness, requests, etc.

# === Concurrency & Thread Settings ===
DEFAULT_THREADS=100                    # Optimal thread count (used by EyeWitness, future fuzzers)

# === Nmap Defaults ===
NMAP_TOP_PORTS=1000                    # Default number of top ports to scan
NMAP_FULL_PORTS="-p-"                  # Full port range
NMAP_SCAN_SPEED="T4"                   # Nmap timing template (T1-T5)

# === WHOIS Settings ===
WHOIS_TIMEOUT=15                       # Timeout if extended WHOIS tools are used in future

# === Subdomain Merge Settings ===
AUTO_MERGE=true                        # If true, automatically merges amass + subfinder

# === Logging & Debugging ===
DEBUG_MODE=false                       # Verbose internal debug logging (for developers)
LOG_TO_FILE=true                       # Save logs to /VAJRA-results/<target>/Logs
VAJRA_JSON=true                        # Enable structured JSON logging in /VAJRA-results/<target>/Final_Summary

# === Console Output & UI ===
USE_COLOR=true                         # If true, allows colored output using ANSI codes
SHOW_BANNER=true                       # Show animated banner on startup

# === Validation Rules ===
DOMAIN_REGEX="^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"  # Basic regex to validate domains

# === Default Tool Paths (override if not in $PATH) ===
EYEWITNESS_PATH="/usr/bin/EyeWitness"  # Modify if installed elsewhere (used by 06-screenshotter.sh)

# === Future Toggles (reserved) ===
ENABLE_CVE_SCANNER=false               # Placeholder toggle for future modules
ENABLE_REPORTING=true                  # Whether to build reports (Phase 3)
