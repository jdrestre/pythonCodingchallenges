"""Módulo que muestra la potencia de un número"""


def power(base, exp):
    """Fx que imprime la potencia de un número dado la base y el exponente."""
    if exp == 0:
        return 1
    return base * power(base, exp - 1)


baseCal = int(input("Enter the base number: "))
exponente = int(input("Enter de exponent: "))

print(power(baseCal, exponente))
