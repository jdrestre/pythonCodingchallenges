"""Imprimir felicidades para los musulmanas"""
import random
import pyfiglet
from termcolor import colored

def eid_al_fitr_wishes():
    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    ascii_art = pyfiglet.figlet_format("Eid Mubarak!", font="slant")
    print(colored(ascii_art, color=random.choice(colors)))

eid_al_fitr_wishes()
