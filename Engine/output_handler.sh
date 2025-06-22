#!/bin/bash

# Output Handler Script for VAJRA Recon Framework
# Purpose: Manage styled, colored, and optionally logged or JSON-formatted output
# Author: YJ

register_module_output() {
    local DIR="$1"
    echo "$DIR" >> "$VAJRA_PATH/core/module_outputs.conf"
}

# === Emoji/Icon Constants ===
TICK="✔"
CROSS="✖"
INFO="ℹ"
WARN="⚠"
ARROW="➤"
SECTION="█"

# === Color Functions ===
bold()    { echo -e "\033[1m$1\033[0m"; }
green()   { echo -e "\033[1;32m$1\033[0m"; }
red()     { echo -e "\033[1;31m$1\033[0m"; }
yellow()  { echo -e "\033[1;33m$1\033[0m"; }
blue()    { echo -e "\033[1;34m$1\033[0m"; }
gray()    { echo -e "\033[1;30m$1\033[0m"; }

# === Output Control Variables (expect VAJRA_OUTPUT_DIR to be set externally) ===
LOG_FILE="$VAJRA_OUTPUT_DIR/output.log"
JSON_OUTPUT="${VAJRA_JSON:-false}"

# === Core Output Functions ===
output_info() {
    local msg="$1"
    local styled="[${INFO}] $(blue "$msg")"
    echo -e "$styled"
    [[ -n "$LOG_FILE" ]] && echo "[INFO] $msg" >> "$LOG_FILE"
    [[ "$JSON_OUTPUT" == true ]] && echo "{\"type\":\"info\",\"message\":\"$msg\"}" >> "$LOG_FILE.json"
}

output_success() {
    local msg="$1"
    local styled="[${TICK}] $(green "$msg")"
    echo -e "$styled"
    [[ -n "$LOG_FILE" ]] && echo "[SUCCESS] $msg" >> "$LOG_FILE"
    [[ "$JSON_OUTPUT" == true ]] && echo "{\"type\":\"success\",\"message\":\"$msg\"}" >> "$LOG_FILE.json"
}

output_error() {
    local msg="$1"
    local styled="[${CROSS}] $(red "$msg")"
    echo -e "$styled"
    [[ -n "$LOG_FILE" ]] && echo "[ERROR] $msg" >> "$LOG_FILE"
    [[ "$JSON_OUTPUT" == true ]] && echo "{\"type\":\"error\",\"message\":\"$msg\"}" >> "$LOG_FILE.json"
}

output_warn() {
    local msg="$1"
    local styled="[${WARN}] $(yellow "$msg")"
    echo -e "$styled"
    [[ -n "$LOG_FILE" ]] && echo "[WARNING] $msg" >> "$LOG_FILE"
    [[ "$JSON_OUTPUT" == true ]] && echo "{\"type\":\"warning\",\"message\":\"$msg\"}" >> "$LOG_FILE.json"
}

output_debug() {
    local msg="$1"
    [[ "$VAJRA_DEBUG" == true ]] && echo -e "[DEBUG] $(gray "$msg")"
    [[ "$LOG_FILE" ]] && [[ "$VAJRA_DEBUG" == true ]] && echo "[DEBUG] $msg" >> "$LOG_FILE"
}

output_section() {
    local title="$1"
    local underline="════════════════════════════════════════"
    echo -e "\n$(bold "[${SECTION}] $(blue "$title")")"
    echo -e "$(gray "$underline")"
    [[ -n "$LOG_FILE" ]] && echo -e "\n[SECTION] $title" >> "$LOG_FILE"
    [[ "$JSON_OUTPUT" == true ]] && echo "{\"type\":\"section\",\"title\":\"$title\"}" >> "$LOG_FILE.json"
}
