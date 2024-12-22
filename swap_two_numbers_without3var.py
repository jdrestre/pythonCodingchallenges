"""
Programa para intercambiar dos números sin utilizar una tercera variable temporal
"""


def swap_numbers(a, b):
    """
    La función `swap_numbers` toma dos número como entrada y los intercambia sin 
    utilizar una tercera variable temporal.
    """
    a = a + b
    b = a - b
    a = a - b
    return a, b


num1 = int(input("Ingrese el primer número: "))
num2 = int(input("Ingrese el segundo número: "))

num1, num2 = swap_numbers(num1, num2)
print(f"Después del intercambio: num1 = {num1}, num2 = {num2}")
