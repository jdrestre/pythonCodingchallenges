"""
Programa de python para convertir centímetro a píes con pulgadas
"""


def conversion(longitud_cm):
    """
    Convierte una longitud de centímetros a píes y pulgadas
    """
    pulgadas_totales = longitud_cm / 2.54
    feet = pulgadas_totales // 12
    inches = pulgadas_totales % 12
    return feet, inches


cm = float(input("Ingrese longitud en centímetro: "))

pies, pulgadas = conversion(cm)

print(f"{cm} cm es aprox. {pies} píes con{pulgadas: .2f} pulgadas")
