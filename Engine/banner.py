'''
def display():
    """Display the VAJRA ASCII banner."""
    banner_text = """
    ██╗   ██╗ █████╗ ██╗   ██╗██████╗  █████╗
    ██║   ██║██╔══██╗██║   ██║██╔══██╗██╔══██╗
    ██║   ██║███████║██║   ██║██████╔╝███████║
    ╚██╗ ██╔╝██╔══██║██║   ██║██╔══██╗██╔══██║
     ╚████╔╝ ██║  ██║╚██████╔╝██║  ██║██║  ██║
      ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
    Multi-layered Red Team Reconnaissance Framework
    """
    print(banner_text)
'''
# VAJRA Rainbow ASCII Banner
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def display_banner():
    """Display the VAJRA rainbow ASCII banner."""
    banner = f"""
    {Fore.RED}██╗   ██╗ {Fore.YELLOW}█████╗ {Fore.GREEN}      ██╗{Fore.CYAN}██████╗  {Fore.BLUE}█████╗
    {Fore.RED}██║   ██║{Fore.YELLOW}██╔══██╗{Fore.GREEN}      ██║{Fore.CYAN}██╔══██╗{Fore.BLUE}██╔══██╗
    {Fore.RED}██║   ██║{Fore.YELLOW}███████║{Fore.GREEN}      ██║{Fore.CYAN}██████╔╝{Fore.BLUE}███████║
    {Fore.RED}╚██╗ ██╔╝{Fore.YELLOW}██╔══██║{Fore.GREEN}██║   ██║{Fore.CYAN}██╔══██╗{Fore.BLUE}██╔══██║
    {Fore.RED} ╚████╔╝ {Fore.YELLOW}██║  ██║{Fore.GREEN}╚██████╔╝{Fore.CYAN}██║  ██║{Fore.BLUE}██║  ██║
    {Fore.RED}  ╚═══╝  {Fore.YELLOW}╚═╝  ╚═╝ {Fore.GREEN}╚═════╝ {Fore.CYAN}╚═╝  ╚═╝{Fore.BLUE}╚═╝  ╚═╝
 {Style.BRIGHT}{Fore.MAGENTA}Multi-layered Red Team Reconnaissance Framework
    {Style.BRIGHT}{Fore.RED}            ＯＷＮＥＲ － ＹＪ
    {Style.RESET_ALL}
    """
    print(banner)
