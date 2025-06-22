#!/bin/bash

# ╔════════════════════════════════════════════════════════╗
# ║ ✅ Complete                                            ║
# ║ 05-nmap.sh — VAJRA Module                              ║
# ║ Description : Scan alive subdomains using Nmap         ║
# ║ Author      : YJ                                       ║
# ╚════════════════════════════════════════════════════════╝

# === Load Environment and Output Tools ===
source "$(dirname "$0")/../Engine/output_handler.sh"
source "$(dirname "$0")/../Utils/config.sh"

MODULE_NAME="nmap"
MODULE_DESC="🧪 Port scanning & service detection using Nmap"
print_module_header "$MODULE_NAME" "$MODULE_DESC"

# === Define Output Paths ===
ALIVE_FILE="$VAJRA_RESULTS/$TARGET/03-Probing/alive.txt"
SCAN_DIR="$VAJRA_RESULTS/$TARGET/04-Scanning"
PER_HOST_DIR="$SCAN_DIR/Per_Host"
METADATA_FILE="$SCAN_DIR/metadata.txt"
SUMMARY_FILE="$SCAN_DIR/all_data.txt"
FAILED_LOG="$VAJRA_RESULTS/$TARGET/Logs/failed_nmap.txt"

mkdir -p "$PER_HOST_DIR" "$VAJRA_RESULTS/$TARGET/Logs"

# === Pre-checks ===
if [[ ! -f "$ALIVE_FILE" ]]; then
    log_error "Missing alive.txt. Please run 03-httprobe.sh first."
    exit 1
fi

LIVE_COUNT=$(wc -l < "$ALIVE_FILE" | xargs)
log_info "Found $LIVE_COUNT alive subdomains to scan."

# === Nmap Mode Selection ===
if [[ -z "$VAJRA_NMAP_MODE" ]]; then
    echo -e "\nChoose Nmap Scan Type:"
    echo "[1] Default     - fast & safe"
    echo "[2] Full        - deep full-port scan"
    echo "[3] Aggressive  - noisy but detailed"
    read -p "Enter choice [1-3]: > " mode_choice

    case "$mode_choice" in
        1) VAJRA_NMAP_MODE="default" ;;
        2) VAJRA_NMAP_MODE="full" ;;
        3) VAJRA_NMAP_MODE="aggressive" ;;
        *) echo "[!] Invalid input. Using default scan."; VAJRA_NMAP_MODE="default" ;;
    esac
fi

# === Configure Scan Flags ===
case "$VAJRA_NMAP_MODE" in
    default)
        SCAN_MODE="default"
        NMAP_FLAGS="-T4 -Pn --top-ports 1000 -sS -sV -sC -O --traceroute --reason"
        TXT_OUT="$SCAN_DIR/default.txt"
        XML_OUT="$SCAN_DIR/default.xml"
        ;;
    full)
        SCAN_MODE="full"
        NMAP_FLAGS="-T4 -Pn -p- -sS -sV -sC -O --traceroute --reason"
        TXT_OUT="$SCAN_DIR/full.txt"
        XML_OUT="$SCAN_DIR/full.xml"
        ;;
    aggressive)
        SCAN_MODE="aggressive"
        NMAP_FLAGS="-T4 -Pn -A --reason"
        TXT_OUT="$SCAN_DIR/aggressive.txt"
        XML_OUT="$SCAN_DIR/aggressive.xml"
        ;;
    *)
        SCAN_MODE="default"
        NMAP_FLAGS="-T4 -Pn --top-ports 1000 -sS -sV -sC -O --traceroute --reason"
        TXT_OUT="$SCAN_DIR/default.txt"
        XML_OUT="$SCAN_DIR/default.xml"
        ;;
esac

print_section "📡 Starting Nmap scan on alive subdomains"
log_info "Scan mode       : $SCAN_MODE"
log_info "Nmap flags used : $NMAP_FLAGS"

# === Start Nmap Scan ===
START_TIME=$(date '+%Y-%m-%d %H:%M:%S')
START_EPOCH=$(date +%s)

nmap -iL "$ALIVE_FILE" $NMAP_FLAGS -oN "$TXT_OUT" -oX "$XML_OUT" > /dev/null 2>&1

# === Parse Results Per Host ===
> "$SUMMARY_FILE"

while read -r DOMAIN; do
    OUT_FILE="$PER_HOST_DIR/$DOMAIN.txt"
    grep -A 20 "$DOMAIN" "$TXT_OUT" > "$OUT_FILE"

    if [[ ! -s "$OUT_FILE" ]]; then
        echo "[!] No open ports or scan failed for $DOMAIN" > "$OUT_FILE"
        echo "$DOMAIN" >> "$FAILED_LOG"
    fi

    echo "========== [$DOMAIN] ==========" >> "$SUMMARY_FILE"
    cat "$OUT_FILE" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"
done < "$ALIVE_FILE"

# === Metadata Summary ===
END_TIME=$(date '+%Y-%m-%d %H:%M:%S')
END_EPOCH=$(date +%s)
DURATION=$((END_EPOCH - START_EPOCH))

cat <<EOF > "$METADATA_FILE"
Scan Mode       : $SCAN_MODE
Target Domain   : $TARGET
Alive Hosts     : $LIVE_COUNT
Nmap Flags Used : $NMAP_FLAGS
Start Time      : $START_TIME
End Time        : $END_TIME
Duration (sec)  : $DURATION
Output Files    : $TXT_OUT, $XML_OUT, Per_Host/*.txt
EOF

log_success "✅ Nmap scan complete for $TARGET"
log_json "$MODULE_NAME" "$TXT_OUT"
