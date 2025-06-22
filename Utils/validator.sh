#!/bin/bash

# ======================================================
# 🔍 VAJRA Utility: validator.sh
# Description : Validates user input for domains, IPs, CIDR, or .txt files
# Supports     :
#   ✅ Single Domain
#   ✅ IPv4 / IPv6
#   ✅ CIDR blocks
#   ✅ .txt files (multiple domains/IPs)
# Author       : YJ (VAJRA Framework)
# ======================================================

is_valid_domain() {
    local domain=$1
    [[ $domain =~ ^(([a-zA-Z0-9-]+)\.)+[a-zA-Z]{2,}$ ]]
}

is_valid_ipv4() {
    local ip=$1
    [[ $ip =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] &&
    awk -F. '{for(i=1;i<=4;i++) if($i<0||$i>255) exit 1}' <<< "$ip"
}

is_valid_ipv6() {
    local ip=$1
    [[ $ip =~ ^([0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4}$ ]]
}

is_valid_cidr() {
    local cidr=$1
    [[ $cidr =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,2}$ ]]
}

is_valid_file() {
    local file=$1
    [[ -f $file && $file == *.txt ]]
}

validate_input() {
    local input=$1

    if is_valid_domain "$input"; then
        echo "domain"
    elif is_valid_ipv4 "$input"; then
        echo "ipv4"
    elif is_valid_ipv6 "$input"; then
        echo "ipv6"
    elif is_valid_cidr "$input"; then
        echo "cidr"
    elif is_valid_file "$input"; then
        echo "file"
    else
        echo "invalid"
    fi
}

# === Example usage ===
# type=$(validate_input "example.com")
# case $type in
#     domain|ipv4|ipv6|cidr)
#         echo "[+] Valid input of type: $type" ;;
#     file)
#         echo "[+] Valid .txt file detected. Reading targets..."
#         while IFS= read -r line; do
#             [[ -z "$line" ]] && continue
#             echo "→ $line"
#         done < "$input"
#         ;;
#     *)
#         echo "[!] Invalid input" ;;
# esac
