"""
Convierte la temperatura: Celsius a Fahrenheit y viceversa. 
Este script permite al usuario convertir temperaturas entre grados Celsius y Fahrenheit. 
El usuario puede elegir entre convertir de Celsius a Fahrenheit o de Fahrenheit a Celsius, 
y el script realizará la conversión y mostrará el resultado. 

Funciones: 
- celsius_to_fahrenheit: Convierte grados Celsius a Fahrenheit. 
- fahrenheit_to_celsius: Convierte grados Fahrenheit a Celsius. 

Uso: 
El usuario elige el tipo de conversión y proporciona la temperatura a convertir. 
El resultado se muestra en pantalla. Cumple con el estándar PEP 8 para estilo de 
código y documentación.
"""


def celsius_to_fahrenheit(temp_celsius):
    """
    Convierte grados Celsius a Fahrenheit, redondea el resultado a un decimal
    """
    return round((temp_celsius * 9/5) + 32, 1)


def fahrenheit_to_celsius(temp_fahrenheit):
    """
    Convierte grados Fahrenheit a Celsius, redondea el resultado a un decimal
    """
    return round((temp_fahrenheit - 32) * 5/9, 1)


# Solicitar al usuario el tipo de conversión
print("Tipo de Conversión")
print("1. Centígrados a Fahrenheit")
print("2. Fahrenheit a Centígrados")
option = int(input("Elige una opción (1 o 2): "))

# Ejecuta la conversión según la opción seleccionada
if option == 1:
    celsius = float(input("Introduce los grados Celsius: "))
    print(f"{celsius} °C son {celsius_to_fahrenheit(celsius)} °F")
elif option == 2:
    fahrenheit = float(input("Introduce los grados Fahrenheit: "))
    print(f"{fahrenheit} °F son {fahrenheit_to_celsius(fahrenheit)} °C")
else:
    print("Opción no válida. Por favor, elige 1 o 2")
