"""Crear una clave de números no consecutivos y que no se repitan"""
import random

def generar_clave(longitud):
    if longitud > 10:  # Solo hay 10 dígitos (0-9), así que la longitud máxima es 8
        return "La longitud debe ser 10 o menos."
    numeros = list(range(10))  # Lista de números del 0 al 9
    clave = []
    while len(clave) < longitud:
        num = random.choice(numeros)
        if not clave or (clave and num != clave[-1] + 1 and num != clave[-1] - 1):
        # Verifica que no sea consecutivo
            clave.append(num)
            numeros.remove(num)  # Elimina el número para evitar repeticiones
    return ''.join(map(str, clave))

# Ejemplo de uso
longitud_de_clave = 8  # Define la longitud de la clave que deseas
clave_generada = generar_clave(longitud_de_clave)
print(clave_generada)
