"""
Esta función calcula la longitud de una cadena sin usar la función de la biblioteca.
"""


def length_string_without_library(s):
    """Esta función calcula la longitud de una cadena sin usar la función de la biblioteca.
    """
    length = 0
    for _ in s:
        length += 1
    return length


input_string = input("Ingrese una cadena de texto: ")
LENGTH = length_string_without_library(input_string)
print(f"La longitud de la cadena de texto es: {LENGTH}")
