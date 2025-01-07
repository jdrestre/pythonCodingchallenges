"""
Programa que imprime todas las permutaciones de una cadena de caracteres en orden lexicográfico.
""" # cSpell: ignore lexicográfico permutaciones lexico

def next_permutation(s):
    """
    Función que calcula la siguiente permutación de una cadena de caracteres en 
    orden lexicográfico. # cSpell: ignore lexicográfico permutación
    """
    # Encontramos el primer índice i tal que s[i] < s[i+1]
    i = len(s) - 2
    while i >= 0 and s[i] >= s[i + 1]:
        i -= 1
    if i == -1:
        return None
    # Encontramos el primer índice j tal que s[j] > s[i]
    j = len(s) - 1
    while s[j] <= s[i]:
        j -= 1
    # Intercambiamos s[i] y s[j]
    s[i], s[j] = s[j], s[i]
    # Invertimos s[i+1:]
    s[i + 1:] = s[i + 1:][::-1]
    return s

def permutations_string_lexico_order(string, print_permutations=False):
    """
    Función que imprime todas las permutaciones de una cadena de caracteres en 
    orden lexicográfico.
    """
    s = list(string)
    s.sort()
    count = 1  # Iniciar el conteo en 1 para incluir la cadena original
    if print_permutations:
        print("".join(s))
    while True:
        s = next_permutation(s)
        if s is None:
            break
        if print_permutations:
            print("".join(s))
        count += 1
    return count

# Ejemplo de uso
input_string = input("Ingrese una cadena de caracteres: ")
NUM_PERMUTATIONS = permutations_string_lexico_order(input_string, print_permutations=False)
print("Número de permutaciones posibles: ", NUM_PERMUTATIONS)
print("¿Desea imprimir las permutaciones? (S/N)")
respuesta = input().strip().lower()

# Listas de respuestas válidas
respuestas_positivas = ['s', 'sí', 'si', 'y', 'yes']
respuestas_negativas = ['n', 'no']

if respuesta in respuestas_positivas:
    permutations_string_lexico_order(input_string, print_permutations=True)
elif respuesta in respuestas_negativas:
    print("No se imprimirán las permutaciones.")
else:
    print("Respuesta no válida.")
