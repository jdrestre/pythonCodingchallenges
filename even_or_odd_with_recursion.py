""" Programa para verificar si un número es par o impar """


def par_impar(number):
    """ Función para definir si es par o impar """
    if number % 2 == 0:
        print(f"El número {number} es par")
    else:
        print(f"El número {number} es impar")


num = int(input("Ingrese un número: "))

par_impar(num)
