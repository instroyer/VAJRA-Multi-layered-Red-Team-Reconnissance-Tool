# Engine/menu.py
# Menu system and input handling for VAJRA

from .logger import info, success, warning, error
import time
import threading
import sys
import select
from Engine.input_utils import get_input, clear_input_buffer

def main_menu(target):
    """  
    Display the main module selection menu.  
    Returns a string of the user's choice(s).  
    """  

    menu_text = f"""  
    {'='*50}  
    VAJRA Main Menu | Target: {target}  
    {'='*50}  
    [ 0 ] Run All  
    [ 1 ] Whois  
    [ 2 ] Subfinder  
    [ 3 ] Amass  
    [ 4 ] Httpx-toolkit  
    [ 5 ] Nmap  
    [ 6 ] Eyewitness (Screenshot)  

    [ 00 ] Runtime Control Menu  
    [ 000 ] Show Help Menu  
    {'='*50}  
    """

    print(menu_text)

    while True:
        try:
            choice = input("> ").strip()  
            if choice == '000':
                return '000'  
            elif choice == '00':
                return '00'  
            elif choice == '0':
                return '0'  
            elif choice:  
                # Validate multiple choices (e.g., '1 2 4')  
                choices = choice.split()  
                if all(c in '123456' for c in choices):  
                    return choice  
                else:  
                    error("Invalid module selection. Choose from 1-6, separated by spaces.")  
                    info("Type '000' for help.")  
            else:  
                warning("Please enter a choice.")  

        except KeyboardInterrupt:
            raise
        except EOFError:
            raise KeyboardInterrupt

def show_help():
    """Display the help menu with option to return immediately with Enter."""
    help_text = f"""
    {'='*50}
    [ * ] VAJRA HELP MENU
    {'='*50}
    [ + ] Module Selection
    [ - ] Target formats supported:
    L Domain name → example.com
    L Subdomain → test.example.com
    L IP address → 192.168.1.10
    L IP range → 192.168.1.0/24
    L File input → @targets.txt (list of targets)

    [ + ] MODULE DESCRIPTIONS
    [0] Complete Pipeline - Run all modules sequentially

    [1] Whois - Domain registration intelligence
    [2] Subfinder - Passive subdomain discovery
    [3] Amass - Comprehensive subdomain enumeration
    [4] HTTPX - Live web service verification
    [5] Nmap - Port scanning & service detection
    [6] Screenshot - Visual reconnaissance

    [ - ] Usage Examples:
        0 → Run all modules in sequence
        1 2 4 → Run Whois + Subfinder + HTTPX
        1 → Run Whois
        000 → Show this Help Menu

    [ + ] Runtime Control (during execution)
    [ - ] Trigger: 00 + ENTER
    [ - ] Actions:
        p → Pause current module
        r → Resume paused module
        s → Skip current module
        q → Quit VAJRA entirely
    [ - ] Any other key → Exit Runtime Menu

    [ + ] Notes
    [ - ] Reports are saved under: Results/Target_YYYYMMDD_HHMMSS/Reports/
    [ - ] Nmap has its own submenu for scan type selection
    [ - ] Screenshots are saved under: Results/Target_YYYYMMDD_HHMMSS/Screenshots/
    {'='*50}
    Press Enter to return immediately or wait 15 seconds...
    """
    print(help_text)

    # Wait for Enter key or timeout
    try:
        for i in range(15, 0, -1):
            # Check if Enter key is pressed
            if sys.stdin in select.select([sys.stdin], [], [], 1)[0]:
                line = sys.stdin.readline()
                if line:  # Enter was pressed
                    print(" " * 30, end='\r')  # Clear the countdown line
                    return
            print(f"Auto-returning in {i} seconds...", end='\r')
        print(" " * 30, end='\r')  # Clear the countdown line
    except KeyboardInterrupt:
        print(" " * 30, end='\r')  # Clear the countdown line
        return
