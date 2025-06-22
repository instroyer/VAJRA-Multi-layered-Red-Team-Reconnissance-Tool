#!/bin/bash

# ============================================
# 🌍 VAJRA Core Script: env_setup.sh
# Description : Environment loader for VAJRA modules
# Author      : YJ (VAJRA Framework)
# ============================================

# === Load global configuration (timeout, threads, etc.) ===
source "$(dirname "$0")/../Utils/config.sh"

# === Validate $TARGET ===
if [[ -z "$TARGET" ]]; then
    echo "[!] TARGET variable not set. Exiting."
    exit 1
fi

# === Set Base Output Directory ===
VAJRA_RESULTS="/VAJRA-results"
RESULTS_DIR="$VAJRA_RESULTS/$TARGET"

# === Set Common Output Paths ===
LOGS_DIR="$RESULTS_DIR/Logs"
INTEL_DIR="$RESULTS_DIR/01-Whois"
SUBDOMAIN_DIR="$RESULTS_DIR/02-Subdomains"
PROBING_DIR="$RESULTS_DIR/03-Probing"
SCANNING_DIR="$RESULTS_DIR/04-Scanning"
SCREENSHOT_DIR="$RESULTS_DIR/05-Screenshots"
FINAL_JSON_DIR="$RESULTS_DIR/Final_Summary"
REPORT_DIR="$RESULTS_DIR/Reports"

# === Ensure All Folders Exist ===
mkdir -p \ 
    "$LOGS_DIR" \ 
    "$INTEL_DIR" \ 
    "$SUBDOMAIN_DIR" \ 
    "$PROBING_DIR" \ 
    "$SCANNING_DIR/Per_Host" \ 
    "$SCREENSHOT_DIR" \ 
    "$FINAL_JSON_DIR" \ 
    "$REPORT_DIR"

# === Export paths so they work in subprocesses ===
export VAJRA_RESULTS
export RESULTS_DIR
export LOGS_DIR
export INTEL_DIR
export SUBDOMAIN_DIR
export PROBING_DIR
export SCANNING_DIR
export SCREENSHOT_DIR
export FINAL_JSON_DIR
export REPORT_DIR
