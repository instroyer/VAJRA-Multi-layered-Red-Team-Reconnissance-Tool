#!/bin/bash

# ======================================
# 🎨 VAJRA Shared Color Palette
# Description : Centralized ANSI styling for all modules
# Author      : YJ (VAJRA Framework)
# ======================================

# === Reset & Text Styles ===
RESET="\033[0m"
BOLD="\033[1m"
UNDERLINE="\033[4m"

# === Basic Colors ===
BLACK="\033[0;30m"
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
MAGENTA="\033[0;35m"
CYAN="\033[0;36m"
WHITE="\033[1;37m"

# === Bright Variants ===
BRIGHT_RED="\033[91m"
BRIGHT_GREEN="\033[92m"
BRIGHT_YELLOW="\033[93m"
BRIGHT_BLUE="\033[94m"
BRIGHT_MAGENTA="\033[95m"
BRIGHT_CYAN="\033[96m"

# === Background Colors (if needed) ===
BG_RED="\033[41m"
BG_GREEN="\033[42m"
BG_YELLOW="\033[43m"
BG_BLUE="\033[44m"
BG_MAGENTA="\033[45m"
BG_CYAN="\033[46m"
BG_WHITE="\033[47m"

# === Status Styles ===
COLOR_SUCCESS="$GREEN"
COLOR_ERROR="$RED"
COLOR_WARN="$YELLOW"
COLOR_INFO="$CYAN"

# === Usage:
# echo -e "${GREEN}[+] Task completed${RESET}"
# echo -e "${BOLD}${RED}[!] Error occurred${RESET}"

# Note:
# This file is sourced in: output_handler.sh, helpers.sh, etc.
# DO NOT use for banner.sh gradients — handled separately there.
