#!/bin/bash

# ============================================
# 📡 VAJRA Module: 03-Amass
# Description : Discover subdomains using Amass in passive mode
# Author      : YJ (VAJRA Framework)
# Status      : ✅ Complete
# ============================================

# === Load core VAJRA components ===
source "$(dirname "$0")/../Engine/output_handler.sh"
source "$(dirname "$0")/../Engine/shortcuts.sh"

# === Handle dry-run from 00-init.sh ===
if [[ "$1" == "--register-only" ]]; then
    register_module_output "Subdomains"
    exit 0
fi

# === Module metadata ===
MODULE_NAME="amass"
MODULE_DESC="📡 Discover subdomains using Amass (passive mode)"
OUTPUT_DIR="$VAJRA_RESULTS/$TARGET/01-Subdomains"

# === Ensure output folder exists ===
mkdir -p "$OUTPUT_DIR"

# === Display a styled module header ===
print_module_header "$MODULE_NAME" "$MODULE_DESC"

# === Start keyboard shortcut listener in background ===
handle_shortcuts &
SHORTCUT_PID=$!

# === Begin Amass Passive Scan ===
log_info "Running Amass (passive mode) on target: $TARGET"
log_info "Saving results to: $OUTPUT_DIR/amass.txt"

amass enum -passive -d "$TARGET" -silent > "$OUTPUT_DIR/amass.txt" 2>/dev/null

# === Check if execution was successful ===
if [[ $? -eq 0 ]]; then
    COUNT=$(wc -l < "$OUTPUT_DIR/amass.txt" | xargs)
    log_success "Amass (passive) completed successfully. Found $COUNT subdomains."
    log_json "$MODULE_NAME" "$OUTPUT_DIR/amass.txt"
else
    log_error "Amass failed on target: $TARGET"
fi

# === Cleanup the keyboard listener ===
kill "$SHORTCUT_PID" 2>/dev/null
