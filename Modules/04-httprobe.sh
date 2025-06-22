#!/bin/bash

# ====================================================================
# 🔌 VAJRA Module: 04-httprobe.sh
# ✅ Complete
# Author: YJ
# Description: Probes live subdomains using httprobe from merged output
# ====================================================================

# === Load core functions ===
source "$(dirname "$0")/../Engine/output_handler.sh"
source "$(dirname "$0")/../Engine/shortcuts.sh"

# === Handle init.sh folder registration ===
if [[ "$1" == "--register-only" ]]; then
    register_module_output "Probing"
    exit 0
fi

# === Module config ===
MODULE_NAME="httprobe"
MODULE_DESC="🔌 Probe live subdomains from Subfinder + Amass"
SUBDOMAIN_DIR="$VAJRA_RESULTS/$TARGET/01-Subdomains"
PROBED_DIR="$VAJRA_RESULTS/$TARGET/03-Probing"
SUBFINDER_FILE="$SUBDOMAIN_DIR/subfinder.txt"
AMASS_FILE="$SUBDOMAIN_DIR/amass.txt"
MERGED_FILE="$SUBDOMAIN_DIR/merged.txt"
PROBED_FILE="$PROBED_DIR/alive.txt"

# === Ensure output folders exist ===
mkdir -p "$PROBED_DIR"

# === Print module header ===
print_module_header "$MODULE_NAME" "$MODULE_DESC"

# === Start shortcut listener ===
handle_shortcuts &
SHORTCUT_PID=$!

# === Step 1: Merge Subfinder + Amass results ===
log_info "Merging Subfinder + Amass output into: $MERGED_FILE"
cat "$SUBFINDER_FILE" "$AMASS_FILE" 2>/dev/null | sed '/^$/d' | sort -u > "$MERGED_FILE"

# === Validate merged list ===
if [[ ! -s "$MERGED_FILE" ]]; then
    log_error "Merged subdomain list is empty. Make sure Subfinder & Amass modules ran successfully."
    kill "$SHORTCUT_PID" 2>/dev/null
    exit 1
fi

COUNT=$(wc -l < "$MERGED_FILE" | xargs)
log_info "Running httprobe on $COUNT unique subdomains..."

# === Step 2: Probe with httprobe ===
cat "$MERGED_FILE" | httprobe -prefer-https -p http:80 -p https:443 > "$PROBED_FILE" 2>/dev/null

# === Step 3: Log results ===
if [[ $? -eq 0 ]]; then
    LIVE_COUNT=$(wc -l < "$PROBED_FILE" | xargs)
    log_success "Httprobe completed. Found $LIVE_COUNT live domains."
    log_json "$MODULE_NAME" "$PROBED_FILE"
else
    log_error "Httprobe failed."
fi

# === Cleanup background shortcut handler ===
kill "$SHORTCUT_PID" 2>/dev/null
