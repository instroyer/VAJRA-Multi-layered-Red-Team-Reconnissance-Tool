#!/bin/bash

# ========================================================
# 📸 VAJRA Module: Screenshotter (Eyewitness-based)
# Description : Captures screenshots of alive domains using EyeWitness
# Author      : YJ (VAJRA Framework)
# ========================================================

# === Load core engine scripts ===
source "$(dirname "$0")/../Engine/output_handler.sh"
source "$(dirname "$0")/../Engine/shortcuts.sh"

# === Module metadata ===
MODULE_NAME="screenshotter"
MODULE_DESC="📸 Capture screenshots of live domains via EyeWitness"
OUTPUT_DIR="$VAJRA_RESULTS/$TARGET/06-Screenshots"
ALIVE_FILE="$VAJRA_RESULTS/$TARGET/04-Probing/alive.txt"

# === Register output directory if init is preparing environment ===
if [[ "$1" == "--register-only" ]]; then
    register_module_output "Screenshots"
    exit 0
fi

# === Ensure output directory exists ===
mkdir -p "$OUTPUT_DIR"

# === Print module header ===
print_module_header "$MODULE_NAME" "$MODULE_DESC"

# === Verify alive.txt exists ===
if [[ ! -s "$ALIVE_FILE" ]]; then
    log_error "Missing or empty alive.txt. Run probing module first."
    exit 1
fi

# === Launch real-time shortcut listener ===
handle_shortcuts &
SHORTCUT_PID=$!

# === Execute EyeWitness ===
log_info "Launching EyeWitness on alive domains..."
log_info "Saving screenshots to: $OUTPUT_DIR"

EyeWitness --web -f "$ALIVE_FILE" \
           --timeout 20 \
           --threads 100 \
           --no-prompt \
           -d "$OUTPUT_DIR" > /dev/null 2>&1

if [[ $? -eq 0 ]]; then
    log_success "EyeWitness completed. Screenshots saved to: $OUTPUT_DIR"
    log_json "$MODULE_NAME" "$OUTPUT_DIR"
else
    log_error "EyeWitness failed or exited with errors."
fi

# === Clean up ===
kill "$SHORTCUT_PID" 2>/dev/null
