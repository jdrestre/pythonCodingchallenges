"""
Programa para revisar si un número es par o impar utilizando `recursion`
"""


def is_even(number):
    """
    Función para identificar si un número es par o impar utilizando `recursion`
    """
    if number == 0:
        return True
    elif number == 1:
        return False
    else:
        return is_even(number - 2)


num = int(input("Ingrese un número: "))

if is_even(num):
    print(f"El número {num} es Par")
else:
    print(f"El número {num} es impar")
