"""
Archivo para definir contraseñas seguras con todos los caracteres posibles y un 
tamaño definido por el usuario
"""
import string
import random


def securityPass(size=8):
    """Función para definir contraseña y tamaño"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # alphabet = string.digits
    password = ''.join(random.choice(alphabet) for _ in range(size))
    return password


security_pass = securityPass(14)
print(f"Contraseña Segura: {security_pass}")
