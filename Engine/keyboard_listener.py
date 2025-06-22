#!/usr/bin/env python3

# ===============================================================
#  VAJRA ENGINE COMPONENT: keyboard_listener.py
#  Author      : YJ
#  Description : Realtime keyboard shortcut handler for VAJRA modules
# ===============================================================

import os
import sys
import tty
import termios
import signal
import time
import select

# ========== Configuration ==========
PARENT_PID = os.getppid()  # The parent Bash script
SHORTCUT_KEYS = ['1', '2', '3', '4', '5', 's', 'r', 'q', 'l', 'd', 'h', 'hh']
VALID_KEYS = ['1', '2', '3', '4', '5', 's', 'r', 'q', 'l', 'd']
HELP_KEYS = ['h', 'hh']

# Signal mapping to parent process
SIGNAL_MAP = {
    '1': signal.SIGUSR1,     # Stop
    '2': signal.SIGUSR2,     # Kill
    '3': signal.SIGCONT,     # Continue
    '4': signal.SIGWINCH,    # Resume
    '5': signal.SIGTSTP,     # Cancel
    's': signal.SIGINT,      # Skip
    'r': signal.SIGTERM,     # Restart
    'q': signal.SIGHUP,      # Quit
    'l': signal.SIGALRM,     # Show Logs
    'd': signal.SIGVTALRM,   # Toggle Debug
    'hh': signal.SIGUSR3     # Show Help
}

# ========== Terminal Colors ==========
RESET = "\033[0m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
MAGENTA = "\033[1;35m"

# ========== Capture single key with timeout ==========
def get_key(timeout):
    """Waits for a single keypress for up to `timeout` seconds."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        rlist, _, _ = select.select([fd], [], [], timeout)
        if rlist:
            return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None

# ========== UI: Shortcut Menu ==========
def print_shortcut_menu():
    """Prints the quick-access shortcut key menu."""
    print(f"\n{CYAN}[+] Shortcut Menu:{RESET}")
    print(f"[{RED}1{RESET}] Stop  | [{RED}2{RESET}] Kill   | [{CYAN}3{RESET}] Continue | [{CYAN}4{RESET}] Resume  | [{GREEN}5{RESET}] Cancel")
    print(f"[{YELLOW}s{RESET}] Skip  | [{BLUE}r{RESET}] Restart | [{MAGENTA}q{RESET}] Quit     | [{CYAN}l{RESET}] Logs    | [{CYAN}d{RESET}] Debug | [{BLUE}hh{RESET}] Help")

# ========== UI: Help Table ==========
def print_help_table():
    """Prints the detailed help menu."""
    print(f"\n{CYAN}[+] Shortcut Help:{RESET}")
    print("| Key | Action Description        |")
    print("|-----|---------------------------|")
    print("|  1  | Stop current module       |")
    print("|  2  | Kill tool process         |")
    print("|  3  | Continue (default)        |")
    print("|  4  | Resume last skipped task  |")
    print("|  5  | Cancel selection (return) |")
    print("|  s  | Skip current tool         |")
    print("|  r  | Restart this module       |")
    print("|  q  | Quit entire framework     |")
    print("|  l  | Show live log             |")
    print("|  d  | Toggle debug mode         |")
    print("| hh  | Show help menu again      |\n")

# ========== Core Listener Loop ==========
def listen():
    """Main keyboard listener logic with 10 second timeout."""
    print_shortcut_menu()
    start_time = time.monotonic()
    timeout = 10
    show_help = False

    while time.monotonic() - start_time < timeout:
        key = get_key(0.5)
        if key is None:
            continue

        # Handle double-key 'hh' (extended help)
        if key == 'h':
            next_key = get_key(1)
            if next_key == 'h':
                print_help_table()
                show_help = True
                start_time = time.monotonic()  # extend time after help
                continue
            elif next_key and next_key in VALID_KEYS:
                os.kill(PARENT_PID, SIGNAL_MAP[next_key])
                return

        # Handle valid shortcut keys
        elif key in VALID_KEYS:
            os.kill(PARENT_PID, SIGNAL_MAP[key])
            return

        # Quit immediately
        elif key == 'q':
            os.kill(PARENT_PID, SIGNAL_MAP[key])
            return

        # Ignore other keys if help was shown
        elif show_help:
            continue

    # Timeout fallback: Resume execution
    os.kill(PARENT_PID, signal.SIGCONT)

# ========== Entry Point ==========
if __name__ == '__main__':
    try:
        listen()
    except KeyboardInterrupt:
        os.kill(PARENT_PID, signal.SIGCONT)
        sys.exit(0)
