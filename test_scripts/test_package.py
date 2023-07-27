import colorama
from colorama import Fore, Back, Style

# Initialize colorama to work with Windows (automatically adds ANSI color codes)
colorama.init()

print(Fore.RED + "This text is in red.")
print(Fore.GREEN + "This text is in green.")
print(Fore.YELLOW + "This text is in yellow.")
# print(Back.BLUE + Fore.WHITE + "This text has blue background and white foreground.")
# print(Style.RESET_ALL + "This text has the default colors.")