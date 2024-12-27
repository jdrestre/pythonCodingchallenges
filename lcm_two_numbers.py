"""
Programa en python para encontrar el MCM Mínimo Común Múltiplo de dos números
"""
import math


def find_lcm(num1, num2):
    """ Función para buscar el LCM de dos números """
    gcd = math.gcd(num1, num2)
    lcm = (num1 * num2) // gcd
    return lcm


number1 = int(input("Ingrese el primer número: "))
number2 = int(input("Ingrese el segundo número: "))

result = find_lcm(number1, number2)
print(f"El MCM de {number1} y {number2} es {result}")
