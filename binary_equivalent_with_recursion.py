"""
Programa para imprimir el equivalente binario de un número entero utilizando 
recursion
"""


def binary_equivalent(number):
    """
    La función `binary_equivalent` convierte un número entero a su
    equivalente binario de forma recursiva.
    """
    if number == 0:
        return "0"
    if number > 0:
        return binary_equivalent_positive(number)
    else:
        return binary_equivalent_negative(number)


def binary_equivalent_positive(number):
    """
    Convierte un número entero positivo a su equivalente binario de forma recursiva.
    """
    if number == 0:
        return ""
    return binary_equivalent_positive(number // 2) + str(number % 2)


def binary_equivalent_negative(number):
    """
    Convierte un número entero negativo a su equivalente binario utilizando el
    complemento a dos de forma recursiva.
    """
    positive_binary = binary_equivalent_positive(
        abs(number))  # Convierte el valor absoluto a binario
    # Invertir los bits (complemento a uno)
    inverted_binary = ''.join(
        '1' if bit == '0' else '0' for bit in positive_binary)
    # Sumar 1 al resultado invertido
    # Asegurar al menos 8 bits (opcional)
    return add_binary(inverted_binary, '1').zfill(4)


def add_binary(bin1, bin2):
    """
    Suma dos números binarios representados como cadenas.
    """
    max_len = max(len(bin1), len(bin2))
    bin1 = bin1.zfill(max_len)
    bin2 = bin2.zfill(max_len)

    result = ''
    carry = 0

    for i in range(max_len - 1, -1, -1):
        r = carry
        r += 1 if bin1[i] == '1' else 0
        r += 1 if bin2[i] == '1' else 0
        result = ('1' if r % 2 == 1 else '0') + result
        carry = 0 if r < 2 else 1

    if carry != 0:
        result = '1' + result

    return result.zfill(max_len)


# Ejemplo de uso:
num = int(input("Ingrese un número entero para convertir a binario: "))
print(f"El binario equivalente de {num} es {binary_equivalent(num)}")
