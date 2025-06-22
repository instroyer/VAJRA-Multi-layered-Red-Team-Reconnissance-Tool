#!/bin/bash

# ================================================
# ⚙️ VAJRA Module: Initialization & Environment Prep
# Description : Sets up base folder structure and checks environment
# Author      : YJ (VAJRA Framework)
# ================================================

# === Load core setup and logging tools ===
source "$(dirname "$0")/../Engine/output_handler.sh"
source "$(dirname "$0")/../Engine/shortcuts.sh"

# === Module metadata ===
MODULE_NAME="init"
MODULE_DESC="⚙️ Initial environment setup and structure creation"

# === Display banner ===
print_module_header "$MODULE_NAME" "$MODULE_DESC"

# === Validate required environment variables ===
if [[ -z "$TARGET" ]]; then
    print_error "❌ TARGET domain not set. Please export TARGET first."
    exit 1
fi

# === Print current configuration ===
log_info "Starting initialization for target: $TARGET"
log_info "VAJRA_RESULTS directory: $VAJRA_RESULTS"

# === Define expected folders per target ===
TARGET_DIR="$VAJRA_RESULTS/$TARGET"

FOLDERS=(
    "$TARGET_DIR/01-Whois"
    "$TARGET_DIR/02-Subdomains"
    "$TARGET_DIR/03-Probing"
    "$TARGET_DIR/04-Scanning/Per_Host"
    "$TARGET_DIR/05-Screenshots"
    "$TARGET_DIR/06-Final_Summary"
    "$TARGET_DIR/07-Reports"
    "$TARGET_DIR/08-Logs"
)

# === Create folder structure ===
for DIR in "${FOLDERS[@]}"; do
    mkdir -p "$DIR"
done

log_success "Target folder structure created for: $TARGET"

# === Create log and metadata placeholders ===
touch "$TARGET_DIR/08-Logs/error.log"
touch "$TARGET_DIR/08-Logs/module_timestamps.log"
touch "$TARGET_DIR/08-Logs/notes.txt"

log_info "Initialized base logs and notes."

# === Optional: validate tools exist ===
REQUIRED_TOOLS=(whois subfinder amass httprobe nmap eyewitness)
for tool in "${REQUIRED_TOOLS[@]}"; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        log_warn "Tool '$tool' not found in PATH. Please install before proceeding."
    fi
done

log_success "✅ Initialization module complete."
