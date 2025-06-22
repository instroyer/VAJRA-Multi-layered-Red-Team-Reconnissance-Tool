#!/bin/bash

# ==================================================
# 🛠️ VAJRA Helpers - Reusable utility functions
# Author      : YJ
# Description : Shared functions used by modules and core scripts
# ==================================================

# === Color Setup (for optional direct echo styling) ===
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
CYAN="\033[1;36m"
RESET="\033[0m"

# === Check if a command exists ===
check_dependency() {
    local CMD="$1"
    if ! command -v "$CMD" >/dev/null 2>&1; then
        echo -e "${RED}[✘] Missing dependency: $CMD${RESET}"
        return 1
    fi
    return 0
}

# === Validate domain syntax ===
validate_domain() {
    local DOMAIN="$1"
    if [[ "$DOMAIN" =~ ^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$ ]]; then
        return 0
    else
        echo -e "${RED}[!] Invalid domain format: $DOMAIN${RESET}"
        return 1
    fi
}

# === Count lines in a file (with error check) ===
count_lines() {
    local FILE="$1"
    if [[ -f "$FILE" ]]; then
        wc -l < "$FILE" | xargs
    else
        echo "0"
    fi
}

# === Merge subfinder + amass results ===
merge_subdomain_files() {
    local SUBFINDER_FILE="$1"
    local AMASS_FILE="$2"
    local OUTPUT_FILE="$3"

    cat "$SUBFINDER_FILE" "$AMASS_FILE" 2>/dev/null | \
        sed '/^$/d' | sort -u > "$OUTPUT_FILE"

    echo "[i] Merged subdomains saved to: $OUTPUT_FILE"
}

# === Extract root domain (strip subdomain) ===
# Input: sub.example.com → Output: example.com
extract_root_domain() {
    local DOMAIN="$1"
    echo "$DOMAIN" | awk -F. '{if (NF>2) print $(NF-1)"."$NF; else print $0}'
}

# === Trim protocol from full URL ===
# Input: https://example.com → Output: example.com
strip_protocol() {
    local URL="$1"
    echo "$URL" | sed -E 's~https?://~~' | cut -d/ -f1
}

# === Format timestamp ===
get_timestamp() {
    date "+%Y-%m-%d %H:%M:%S"
}

# === Debug print (optional toggle via $DEBUG_MODE) ===
debug_log() {
    local MSG="$1"
    [[ "$DEBUG_MODE" == "true" ]] && echo -e "${YELLOW}[DEBUG] $MSG${RESET}"
}

# === Banner (optional use) ===
print_banner_line() {
    echo -e "${CYAN}───────────────────────────────────────────────${RESET}"
}

