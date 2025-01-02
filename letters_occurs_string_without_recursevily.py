"""
Este módulo cuenta las ocurrencias de una letra específica dentro de una cadena 
dada sin usar recursividad.
"""


def count_letter(s, letter):
    """
    La función `count_letter` cuenta las ocurrencias de una letra específica 
    dentro de una cadena dada sin usar recursividad.
    """
    letter_count = 0
    for char in s:
        if char == letter:
            letter_count += 1
    return letter_count


input_string = input("Ingrese una cadena de texto: ")
input_letter = input("Ingrese la letra a contar: ")

if len(input_letter) != 1:
    print("Por favor ingrese solo una letra")
else:
    count = count_letter(input_string, input_letter)
    print(f"La letra '{input_letter}' se repite {
          count} veces dentro de la cadena de texto.")
