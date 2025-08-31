# Engine/menu_logger.py 

import sys
import time
from colorama import Fore, Style, init

# Initialize colorama
init()

class Logger:
    """MSFconsole-style colored logger"""
    
    @staticmethod
    def info(message):
        print(f"{Fore.CYAN}[ * ]{Style.RESET_ALL} {message}")
    
    @staticmethod
    def success(message):
        print(f"{Fore.GREEN}[ + ]{Style.RESET_ALL} {message}")
    
    @staticmethod
    def warning(message):
        print(f"{Fore.YELLOW}[ ! ]{Style.RESET_ALL} {message}")
    
    @staticmethod
    def error(message):
        print(f"{Fore.RED}[ - ]{Style.RESET_ALL} {message}")
    
    @staticmethod
    def prompt(message):
        print(f"{Fore.MAGENTA}[ ? ]{Style.RESET_ALL} {message}", end="")

def show_help_menu():
    """Displays the help menu with usage instructions."""
    help_text = f"""
{Fore.MAGENTA}
╔══════════════════════════════════════════════════╗
║                   VAJRA HELP MENU                ║
╚══════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}[ + ] Module Selection{Style.RESET_ALL}
    {Fore.CYAN}•{Style.RESET_ALL} Enter numbers separated by spaces (e.g., '1 2 5')
    {Fore.CYAN}•{Style.RESET_ALL} [ 0 ] = Run all modules in sequence
    {Fore.CYAN}•{Style.RESET_ALL} Choose specific numbers for custom workflow

{Fore.YELLOW}[ + ] Target Format{Style.RESET_ALL}
    {Fore.CYAN}•{Style.RESET_ALL} Single: example.com or 192.168.1.1
    {Fore.CYAN}•{Style.RESET_ALL} Multiple: example.com google.com
    {Fore.CYAN}•{Style.RESET_ALL} File: @targets.txt

{Fore.YELLOW}[ + ] Runtime Control{Style.RESET_ALL}
    {Fore.CYAN}•{Style.RESET_ALL} Press [00] during scan for control menu
    {Fore.CYAN}•{Style.RESET_ALL} Options: Pause, Resume, Skip, Quit

{Fore.YELLOW}[ + ] Reports{Style.RESET_ALL}
    {Fore.CYAN}•{Style.RESET_ALL} Generated in Results/<target>/Reports/
    {Fore.CYAN}•{Style.RESET_ALL} Both HTML and PDF formats available

{Fore.GREEN}Press any key to continue...{Style.RESET_ALL}
"""
    
    print(help_text)
    try:
        input()  # Wait for user to press any key
    except KeyboardInterrupt:
        print("\n")
        return

def show_module_menu():
    """Displays the main module selection menu and returns user choices."""
    
    menu_text = f"""
{Fore.MAGENTA}
╔══════════════════════════════════════════════════╗
║                VAJRA MODULE SELECTION            ║
╚══════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.CYAN}[ 0 ]{Style.RESET_ALL}  All Modules (Complete Recon Pipeline)
{Fore.CYAN}[ 1 ]{Style.RESET_ALL}  Whois Lookup
{Fore.CYAN}[ 2 ]{Style.RESET_ALL}  Subfinder (Subdomain Enumeration)
{Fore.CYAN}[ 3 ]{Style.RESET_ALL}  Amass (Subdomain Enumeration)
{Fore.CYAN}[ 4 ]{Style.RESET_ALL}  HTTPX (Probe Alive Subdomains)
{Fore.CYAN}[ 5 ]{Style.RESET_ALL}  Nmap (Port Scanning)
{Fore.CYAN}[ 6 ]{Style.RESET_ALL}  Screenshot (Capture Websites)

{Fore.YELLOW}[ 000 ]{Style.RESET_ALL} Show Help Menu
{Fore.YELLOW}[ 00 ]{Style.RESET_ALL}  During Scan: Show Control Menu

{Fore.GREEN}Enter your choices (space-separated):{Style.RESET_ALL}
"""
    
    print(menu_text)
    
    while True:
        try:
            choices = input("    > ").strip()
            
            # Check for help command
            if choices == '000':
                show_help_menu()
                print(menu_text)  # Re-show the menu after help
                continue
                
            # Validate input
            if not choices:
                Logger.warning("Please enter at least one choice.")
                continue
                
            choice_list = choices.split()
            
            # Validate each choice
            valid_choices = ['0', '1', '2', '3', '4', '5', '6']
            for choice in choice_list:
                if choice not in valid_choices:
                    Logger.error(f"Invalid choice: {choice}. Please enter numbers 0-6.")
                    break
            else:
                # All choices are valid
                return choice_list
                
        except KeyboardInterrupt:
            Logger.error("Operation cancelled by user.")
            sys.exit(1)
        except Exception as e:
            Logger.error(f"Input error: {e}")

def ask_report_preference():
    """Ask user if they want to generate reports after module completion."""
    Logger.prompt("Generate modular reports after completion? (y/n): ")
    
    while True:
        try:
            choice = input().lower().strip()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                Logger.error("Please enter 'y' or 'n': ")
        except KeyboardInterrupt:
            Logger.error("Operation cancelled.")
            sys.exit(1)

# Example usage and test
if __name__ == "__main__":
    Logger.info("Starting VAJRA Logger Test")
    Logger.success("Test successful!")
    Logger.warning("This is a warning")
    Logger.error("This is an error")
    
    # Test menu display
    choices = show_module_menu()
    print(f"User selected: {choices}")
    
    # Test report preference
    report_choice = ask_report_preference()
    print(f"Generate reports: {report_choice}")
