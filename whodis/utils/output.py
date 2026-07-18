"""Output formatting utilities for WHODIS."""

from colorama import Fore, Back, Style, init
from .config import COLORS, EMOJIS, VERSION

# Initialize colorama
init(autoreset=True)

class Output:
    """Handle colored and formatted output."""

    @staticmethod
    def header():
        """Print application header."""
        dark_red = "\033[31m"
        reset = "\033[0m"
        print(f"\n{dark_red}{'='*60}{reset}")
        print(f"{dark_red}┌─────────────────────────────────────────────────────────┐{reset}")
        print(f"{dark_red}│{reset}  WHODIS — Full OSINT Phone Number Investigator")
        print(f"{dark_red}│{reset}  Version {VERSION}")
        print(f"{dark_red}└─────────────────────────────────────────────────────────┘{reset}")
        print(f"{dark_red}{'='*60}{reset}\n")

    @staticmethod
    def info(message: str):
        """Print info message."""
        print(f"{Fore.CYAN}{EMOJIS['INFO']} {message}{Style.RESET_ALL}")

    @staticmethod
    def success(message: str):
        """Print success message."""
        print(f"{Fore.GREEN}{EMOJIS['CHECK']} {message}{Style.RESET_ALL}")

    @staticmethod
    def error(message: str):
        """Print error message."""
        print(f"{Fore.RED}{EMOJIS['CROSS']} {message}{Style.RESET_ALL}")

    @staticmethod
    def warning(message: str):
        """Print warning message."""
        print(f"{Fore.YELLOW}{EMOJIS['WARNING']} {message}{Style.RESET_ALL}")

    @staticmethod
    def source_result(index: int, total: int, source: str, emoji: str, status: str, details: str = ""):
        """Print source scanning result."""
        status_color = Fore.GREEN if "✅" in status else (Fore.YELLOW if "⏳" in status else Fore.RED)
        detail_str = f" — {details}" if details else ""
        print(f"[{index}/{total}] {emoji} {source:<20} {status_color}{status}{Style.RESET_ALL}{detail_str}")

    @staticmethod
    def separator(char: str = "━", length: int = 60):
        """Print separator line."""
        print(f"{Fore.RED}{char * length}{Style.RESET_ALL}")

    @staticmethod
    def result_box(title: str, data: dict, full_width: bool = True):
        """Print a formatted result box."""
        dark_red = "\033[31m"
        reset = "\033[0m"
        
        print(f"\n{dark_red}┌─────────────────────────────────────────────────────────┐{reset}")
        print(f"{dark_red}│{reset}  {title}")
        print(f"{dark_red}├─────────────────────────────────────────────────────────┤{reset}")
        
        for key, value in data.items():
            if isinstance(value, list):
                print(f"{dark_red}│{reset}  {Fore.CYAN}{key:<20}{Style.RESET_ALL}: ")
                for item in value:
                    print(f"{dark_red}│{reset}    • {item}")
            elif isinstance(value, dict):
                print(f"{dark_red}│{reset}  {Fore.CYAN}{key:<20}{Style.RESET_ALL}:")
                for k, v in value.items():
                    print(f"{dark_red}│{reset}    {k}: {v}")
            else:
                print(f"{dark_red}│{reset}  {Fore.CYAN}{key:<20}{Style.RESET_ALL}: {value}")
        
        print(f"{dark_red}└─────────────────────────────────────────────────────────┘{reset}\n")

    @staticmethod
    def print_results(results: dict, number: str):
        """Print final results in a formatted way."""
        output = Output()
        dark_red = "\033[31m"
        reset = "\033[0m"
        
        # Collect all found data organized by source
        found_sources = {}
        
        for source, result in results.items():
            if result and result.get("found"):
                if result.get("data"):
                    found_sources[source] = result["data"]
        
        # Print header box
        print(f"\n{dark_red}┌─────────────────────────────────────────────────────────┐{reset}")
        print(f"{dark_red}│{reset}  HASIL INVESTIGASI WHODIS")
        print(f"{dark_red}├─────────────────────────────────────────────────────────┤{reset}")
        print(f"{dark_red}│{reset}  {Fore.CYAN}Nomor Target{Style.RESET_ALL:<19}: {number}")
        print(f"{dark_red}│{reset}  {Fore.CYAN}Sumber Ditemukan{Style.RESET_ALL:<14}: {len(found_sources)}/{len(results)}")
        print(f"{dark_red}└─────────────────────────────────────────────────────────┘{reset}\n")
        
        # Print detailed results
        if found_sources:
            print(f"{dark_red}{'='*60}{reset}")
            print(f"{Fore.GREEN}✅ IDENTITAS DITEMUKAN{Style.RESET_ALL}")
            print(f"{dark_red}{'='*60}{reset}\n")
            
            # Display organized data by source
            for source, data in found_sources.items():
                source_name = source.upper()
                print(f"{Fore.YELLOW}📍 {source_name}{Style.RESET_ALL}")
                
                for key, value in data.items():
                    if key == 'source':
                        continue  # Skip source key
                    
                    # Format output based on data type
                    if isinstance(value, list):
                        print(f"   {Fore.CYAN}{key:<20}{Style.RESET_ALL}: ")
                        for item in value:
                            print(f"      • {item}")
                    elif isinstance(value, dict):
                        print(f"   {Fore.CYAN}{key:<20}{Style.RESET_ALL}:")
                        for k, v in value.items():
                            print(f"      {k}: {v}")
                    else:
                        # Clean display for string values
                        display_value = str(value)
                        if len(display_value) > 50:
                            display_value = display_value[:47] + "..."
                        print(f"   {Fore.CYAN}{key:<20}{Style.RESET_ALL}: {display_value}")
                
                print()  # Empty line between sources
            
            print(f"{dark_red}{'='*60}{reset}")
            print(f"{Fore.CYAN}📊 Ringkasan Sumber{Style.RESET_ALL}")
            print(f"{dark_red}{'='*60}{reset}")
            for source in found_sources.keys():
                print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {source.title()}")
            print(f"{dark_red}{'='*60}{reset}\n")
        else:
            print(f"{dark_red}{'='*60}{reset}")
            print(f"{Fore.RED}❌ IDENTITAS TIDAK DITEMUKAN{Style.RESET_ALL}")
            print(f"{dark_red}{'='*60}{reset}\n")
            print(f"{Fore.YELLOW}Nomor valid tetapi tidak terdaftar di sumber mana pun.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Kemungkinan: Nomor privacy, burner number, atau jarang digunakan.{Style.RESET_ALL}\n")
