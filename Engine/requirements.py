#!/bin/bash

# shortcuts.sh — Signal-based shortcut controller for VAJRA

STATUS_FILE="/tmp/vajra_status.flag"

# === Color Codes ===
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[1;34m"
CYAN="\033[1;36m"
MAGENTA="\033[1;35m"
RESET="\033[0m"

# === Setup Signal Traps ===
trap_shortcuts() {
    trap 'handle_stop' SIGUSR1
    trap 'handle_kill' SIGUSR2
    trap 'handle_continue' SIGCONT
    trap 'handle_resume' SIGWINCH
    trap 'handle_cancel' SIGTSTP
    trap 'handle_skip' SIGINT
    trap 'handle_restart' SIGTERM
    trap 'handle_quit' SIGHUP
    trap 'handle_help' SIGUSR3
}

reset_shortcut_flags() {
    echo "running" > "$STATUS_FILE"
}

check_shortcut_status() {
    [[ ! -f "$STATUS_FILE" ]] && echo "running" > "$STATUS_FILE"
    STATUS=$(<"$STATUS_FILE")
    case "$STATUS" in
        "skip")
            echo -e "${YELLOW}[!] Module skipped${RESET}"
            return 1
            ;;
        "stop")
            echo -e "${RED}[!] Module stopped${RESET}"
            exit 1
            ;;
        "kill")
            echo -e "${RED}[!] Tool terminated${RESET}"
            exit 2
            ;;
        "quit")
            echo -e "${MAGENTA}[!] Framework exited${RESET}"
            exit 3
            ;;
    esac
    return 0
}

# === Individual Shortcut Handlers ===

handle_stop() {
    echo -e "${RED}[!] Module stopped${RESET}"
    echo "stop" > "$STATUS_FILE"
}

handle_kill() {
    echo -e "${RED}[!] Framework killed${RESET}"
    echo "kill" > "$STATUS_FILE"
}

handle_continue() {
    echo -e "${CYAN}[~] Continuing...${RESET}"
    echo "running" > "$STATUS_FILE"
}

handle_resume() {
    echo -e "${CYAN}[~] Resuming skipped task...${RESET}"
    echo "resume" > "$STATUS_FILE"
}

handle_cancel() {
    echo -e "${GREEN}[✔] Action canceled${RESET}"
    echo "cancel" > "$STATUS_FILE"
}

handle_skip() {
    echo -e "${YELLOW}[!] Skipping module...${RESET}"
    echo "skip" > "$STATUS_FILE"
}

handle_restart() {
    echo -e "${BLUE}[~] Restarting module...${RESET}"
    echo "restart" > "$STATUS_FILE"
}

handle_quit() {
    echo -e "${MAGENTA}[!] Exiting VAJRA...${RESET}"
    echo "quit" > "$STATUS_FILE"
}

handle_help() {
    # Full shortcut preview (3-line version with color)
    echo -e "${CYAN}[+] Shortcut Menu:${RESET}"
    echo -e "[${RED}1${RESET}] Stop | [${RED}2${RESET}] Kill | [${CYAN}3${RESET}] Continue | [${CYAN}4${RESET}] Resume | [${GREEN}5${RESET}] Cancel"
    echo -e "[${YELLOW}s${RESET}] Skip | [${BLUE}r${RESET}] Restart | [${MAGENTA}q${RESET}] Quit | [${CYAN}l${RESET}] Logs | [${CYAN}d${RESET}] Debug | [${BLUE}hh${RESET}] Help"

    # Full help table
    echo -e "\n${CYAN}[+] Shortcut Help — Available Commands${RESET}\n"
    echo -e "| ${BLUE}Key${RESET} | ${BLUE}Action Description${RESET}        |"
    echo    "|-----|---------------------------|"
    echo    "|  1  | Stop current module       |"
    echo    "|  2  | Kill tool process         |"
    echo    "|  3  | Continue (default)        |"
    echo    "|  4  | Resume last skipped task  |"
    echo    "|  5  | Cancel selection (return) |"
    echo    "|  s  | Skip current tool         |"
    echo    "|  r  | Restart this module       |"
    echo    "|  q  | Quit entire framework     |"
    echo    "|  l  | Show live log             |"
    echo    "|  d  | Toggle debug mode         |"
    echo    "| hh  | Show help (shortcut menu) |"
    echo ""
}
