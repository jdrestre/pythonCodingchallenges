"""
Calcular "Greatest Common Divisor" GCM o "Máximo Común Divisor" MCD sin importar 
módulo `math`
"""


def find_gcd(a, b):
    """ Función para busca GCD """
    while b:
        a, b = b, a % b
    return a


number1 = int(input("Ingrese el primer número: "))
number2 = int(input("Ingrese el segundo número: "))

gcd = find_gcd(number1, number2)
print(f"The GCD of {number1} and {number2} is {gcd}")
