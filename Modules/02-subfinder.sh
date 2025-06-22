#!/bin/bash

# ===================================================
# ✅ VAJRA Module [Complete] — 02-subfinder.sh
# Module Name : Subfinder
# Description : Passive subdomain enumeration using Subfinder
# Author      : YJ (VAJRA Framework)
# ===================================================

# === Load core dependencies ===
source "$(dirname "$0")/../Engine/output_handler.sh"
source "$(dirname "$0")/../Engine/shortcuts.sh"

# === Module metadata ===
MODULE_NAME="subfinder"
MODULE_DESC="🔍 Passive Subdomain Discovery via Subfinder"
OUTPUT_DIR="$VAJRA_RESULTS/$TARGET/02-Subdomains"
SUBFINDER_OUTPUT="$OUTPUT_DIR/subfinder.txt"

# === Register module if only registering ===
if [[ "$1" == "--register-only" ]]; then
    register_module_output "Subdomains"
    exit 0
fi

# === Ensure output folder exists ===
mkdir -p "$OUTPUT_DIR"

# === Print formatted module header ===
print_module_header "$MODULE_NAME" "$MODULE_DESC"

# === Launch background shortcut listener ===
handle_shortcuts &
SHORTCUT_PID=$!

# === Run Subfinder ===
log_info "Running Subfinder on: $TARGET"
subfinder -d "$TARGET" -silent -all > "$SUBFINDER_OUTPUT" 2>/dev/null

# === Validate and log results ===
if [[ $? -eq 0 ]]; then
    COUNT=$(wc -l < "$SUBFINDER_OUTPUT" | xargs)
    log_success "Subfinder completed. Found $COUNT subdomains."
    log_json "$MODULE_NAME" "$SUBFINDER_OUTPUT"
else
    log_error "Subfinder failed for $TARGET."
fi

# === Cleanup ===
kill "$SHORTCUT_PID" 2>/dev/null
