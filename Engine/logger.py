# MSFconsole-style logging utility with full line coloring
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def info(message):
    print(f"{Fore.CYAN}[*]{Style.RESET_ALL} {Fore.CYAN}{message}{Style.RESET_ALL}")

def success(message):
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {Fore.GREEN}{message}{Style.RESET_ALL}")

def warning(message):
    print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} {Fore.YELLOW}{message}{Style.RESET_ALL}")

def error(message):
    print(f"{Fore.RED}[-]{Style.RESET_ALL} {Fore.RED}{message}{Style.RESET_ALL}")

def target_info(message):
    """Special yellow color for target information"""
    print(f"{Fore.YELLOW}[+]{Style.RESET_ALL} {Fore.YELLOW}{message}{Style.RESET_ALL}")
