"""
Imprimir editando el texto con pyfiglet, colorama módulo Fore
"""

from colorama import Fore
import pyfiglet

ascii_art = pyfiglet.figlet_format("Feliz Navidad'", font='dos_rebel')
print(ascii_art)

font = pyfiglet.figlet_format("Feliz Navidad'", font='dos_rebel')
print(Fore.RED + font)

# available_fonts = pyfiglet.FigletFont.getFonts()
# print(available_fonts)

# FONT_COUNT = 0

# for font in available_fonts:
#     FONT_COUNT += 1

# print(F"Número de tipos de letra en figlet: {FONT_COUNT}")
