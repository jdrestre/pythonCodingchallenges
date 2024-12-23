"""
Este programa cuenta el número de bits establecidos (bits en 1) en la representación binaria 
de un número entero ingresado por el usuario.
"""


def count_set_bits(n):
    """
    The function `count_set_bits(n)` calculates the number of set bits (binary 1s)
    in the binary representation of the input integer `n`.
    """
    count = 0
    while n > 0:
        count += n & 1
        n >>= 1
    return count


num = int(input("Ingrese un número entero: "))
print(f"El número de bits establecidos en {num} es {count_set_bits(num)}")
