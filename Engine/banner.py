
# KESTREL ASCII Banner
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def display_banner():
    """Display the KESTREL ASCII banner."""
    banner = f"""
{Fore.RED}██╗  ██╗{Fore.YELLOW}███████╗{Fore.GREEN}███████╗{Fore.CYAN}████████╗{Fore.BLUE}██████╗ {Fore.MAGENTA}███████╗{Fore.RED}██╗
{Fore.RED}██║ ██╔╝{Fore.YELLOW}██╔════╝{Fore.GREEN}██╔════╝{Fore.CYAN}╚══██╔══╝{Fore.BLUE}██╔══██╗{Fore.MAGENTA}██╔════╝{Fore.RED}██║
{Fore.RED}█████╔╝ {Fore.YELLOW}█████╗  {Fore.GREEN}███████╗{Fore.CYAN}   ██║   {Fore.BLUE}██████╔╝{Fore.MAGENTA}█████╗  {Fore.RED}██║
{Fore.RED}██╔═██╗ {Fore.YELLOW}██╔══╝  {Fore.GREEN}╚════██║{Fore.CYAN}   ██║   {Fore.BLUE}██╔══██╗{Fore.MAGENTA}██╔══╝  {Fore.RED}██║
{Fore.RED}██║  ██╗{Fore.YELLOW}███████╗{Fore.GREEN}███████║{Fore.CYAN}   ██║   {Fore.BLUE}██║  ██║{Fore.MAGENTA}███████╗{Fore.RED}███████╗
{Fore.RED}╚═╝  ╚═╝{Fore.YELLOW}╚══════╝{Fore.GREEN}╚══════╝{Fore.CYAN}   ╚═╝   {Fore.BLUE}╚═╝  ╚═╝{Fore.MAGENTA}╚══════╝{Fore.RED}╚══════╝
{Style.BRIGHT}{Fore.YELLOW}           Multi-layered Reconnaissance Tool
{Fore.RED}                   ＯＷＮＥＲ － ＹＪ
{Style.RESET_ALL}
    """
    print(banner)
