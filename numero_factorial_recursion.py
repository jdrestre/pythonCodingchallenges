"""Programa para buscar el número factorial utilizando `recursion`"""


def factorial(n):
    """Calculo el factorial de un número de forma recursiva"""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
num = int(input("Ingrese un número: "))
if num < 0:
    print("El factorial no está definido para números negativos")
print(f"El factorial de {num} es {factorial(num)}.")
