#!/bin/bash

# ===================================================
# ✅ VAJRA Module [Complete] — 01-whois.sh
# Module Name : WHOIS Lookup
# Description : Retrieves WHOIS information of the root domain
# Author      : YJ (VAJRA Framework)
# ===================================================

# === Load core framework dependencies ===
source "$(dirname "$0")/../Engine/output_handler.sh"
source "$(dirname "$0")/../Engine/shortcuts.sh"

# === Module metadata ===
MODULE_NAME="whois"
MODULE_DESC="🧾 WHOIS Lookup for root domain"
OUTPUT_DIR="$VAJRA_RESULTS/$TARGET/01-Whois"
LOG_FILE="$VAJRA_RESULTS/$TARGET/08-Logs/whois.log"
WHOIS_OUTPUT="$OUTPUT_DIR/whois.txt"

# === Register output directory if only registering modules ===
if [[ "$1" == "--register-only" ]]; then
    register_module_output "Whois"
    exit 0
fi

# === Ensure the output folder exists ===
mkdir -p "$OUTPUT_DIR"

# === Print the module header to screen/log ===
print_module_header "$MODULE_NAME" "$MODULE_DESC"

# === Launch shortcut listener in background ===
handle_shortcuts &
SHORTCUT_PID=$!

# === Run WHOIS command and log ===
log_info "Running WHOIS for: $TARGET"
whois "$TARGET" > "$WHOIS_OUTPUT" 2>> "$LOG_FILE"

# === Validate output ===
if [[ -s "$WHOIS_OUTPUT" ]]; then
    log_success "WHOIS info saved to: $WHOIS_OUTPUT"
    log_json "$MODULE_NAME" "$WHOIS_OUTPUT"
else
    log_error "WHOIS returned empty. Check if the domain is valid or reachable."
fi

# === Cleanup shortcut handler ===
kill "$SHORTCUT_PID" 2>/dev/null
