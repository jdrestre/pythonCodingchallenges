"""
Este programa cuenta las ocurrencias de una letra específica dentro de una cadena
"""


def count_letter_recursively(s, letter):
    """
    The function `count_letter_recursively` recursively counts the occurrences 
    of a specific letter within a given string.
    """
    if not s:
        return 0
    return (1 if s[0] == letter else 0) + count_letter_recursively(s[1:], letter)


input_string = input("Ingrese una cadena de texto: ")
input_letter = input("Ingrese la letra a contar: ")

if len(input_letter) != 1:
    print("Por favor ingrese solo una letra")
else:
    count = count_letter_recursively(input_string, input_letter)
    print(f"La letra '{input_letter}' se repite {
          count} veces dentro de la cadena de texto.")
