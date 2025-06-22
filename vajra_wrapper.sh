#!/bin/bash

# ============================================
# 🚀 VAJRA Wrapper Script (Multi-Target Launcher)
# Location   : /VAJRA/vajra_wrapper.sh
# Author     : YJ
# Description: Accepts a file or target list and launches VAJRA modules
# Usage      : bash vajra_wrapper.sh targets.txt
# ============================================

# === Load environment and validator ===
source "$(dirname "$0")/Utils/config.sh"
source "$(dirname "$0")/Utils/validator.sh"

# === Usage Help ===
function usage() {
    echo -e "\nUsage: bash $0 <target | target_list.txt>"
    echo -e "       bash $0 example.com"
    echo -e "       bash $0 targets.txt  # with domains, IPs, CIDRs or .txts"
    exit 1
}

# === Check input ===
[[ -z "$1" ]] && usage
INPUT="$1"

# === Parse input file or single target ===
TARGETS=()
if [[ -f "$INPUT" ]]; then
    while IFS= read -r line; do
        [[ -z "$line" || "$line" =~ ^# ]] && continue
        TARGETS+=("$line")
    done < "$INPUT"
else
    TARGETS+=("$INPUT")
fi

# === Loop through targets ===
for TARGET in "${TARGETS[@]}"; do
    echo -e "\n============================"
    echo -e "🔍 Starting Recon on: $TARGET"
    echo -e "============================"

    # === Validate ===
    if ! validate_target "$TARGET"; then
        echo "[!] Invalid target: $TARGET — Skipping."
        continue
    fi

    # === Set environment ===
    export TARGET="$TARGET"
    export VAJRA_OUTPUT_DIR="$PWD/VAJRA-results"

    # === Start modules (sequentially) ===
    bash Modules/00-init.sh
    bash Modules/01-whois.sh
    bash Modules/02-subfinder.sh
    bash Modules/03-amass.sh
    bash Modules/04-httprobe.sh
    bash Modules/05-nmap.sh
    bash Modules/06-screenshotter.sh

    echo -e "\n✅ Recon complete for: $TARGET"
    echo "Results saved in: $VAJRA_OUTPUT_DIR/$TARGET"

done

exit 0
