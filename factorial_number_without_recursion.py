"""Programa para buscar número factorial sin `recursion`"""

def factorial(n):
    """Calcula el factorial de un número de forma iterativa"""
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

numero = int(input("Ingrese un número para buscar su factorial: "))
print(f"El factorial de {numero} es: {factorial(numero)}.")
