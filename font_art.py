from colorama import Fore
import pyfiglet

ascii_art = pyfiglet.figlet_format("Feliz Navidad'")
print(ascii_art)

font = pyfiglet.figlet_format("Feliz Navidad'")
print(Fore.RED+font)
