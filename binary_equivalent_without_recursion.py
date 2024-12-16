"""Programa para convertir un número entero, positivo o negativo, a binario"""


def integer_to_binary(n):
    """
    La función `integer_to_binary` convierte un número entero a su 
    representación binaria, manejando tanto números positivos como negativos
    """
    if n == 0:
        return "0"

    # Para números negativos, usamos el complemento a dos
    if n < 0:
        # Convertimos el número a positivo
        n = -n
        # Obtenemos la representación binaria del número positivo
        binary_num = ""
        while n > 0:
            binary_num = str(n % 2) + binary_num
            n = n // 2
        # Invertimos los bits (complemento a uno)
        binary_num = ''.join('1' if bit == '0' else '0' for bit in binary_num)
        # Sumamos 1 al resultado para obtener el complemento a dos
        bin_as_int = int(binary_num, 2) + 1
        # Convertimos nuevamente a binario sin usar bin y retornamos el resultado
        binary_num = ""
        while bin_as_int > 0:
            binary_num = str(bin_as_int % 2) + binary_num
            bin_as_int = bin_as_int // 2
        # Aseguramos que el binario negativo tenga un bit inicial negativo según
        # el tamaño (opcional 8 bits)
        return binary_num.zfill(4)
    else:
        # Para números positivos, convertimos directamente a binario
        binary_num = ""
        while n > 0:
            binary_num = str(n % 2) + binary_num
            n = n // 2
        return binary_num


num = int(input("Ingrese un número entero para convertir a binario: "))
print(f"El equivalente binario de {num} es {integer_to_binary(num)}")
