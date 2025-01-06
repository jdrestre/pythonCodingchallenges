"""Programa de python para contar el número de letras y números en una cadena de caracteres"""

# cSpell: ignore numeros, letras
def contar_letras_numeros(cadena):
    """Función para contar el número de letras y números en una cadena de caracteres"""
    letras = 0
    numeros = 0
    for i in cadena:
        if i.isalpha():
            letras += 1
        elif i.isdigit():
            numeros += 1
    return letras, numeros

entrada = input("Introduce una cadena de caracteres: ")
letras_, numeros_ = contar_letras_numeros(entrada)
print("Número de letras: ", letras_)
print("Número de números: ", numeros_)

# Output
# Introduce una cadena de caracteres: 12345abcde
# Número de letras:  5
# Número de números:  5
