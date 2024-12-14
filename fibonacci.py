"""Programa para buscar números de fibonacci utilizando recursion"""


def fibonacci(n):
    """Calcula el enésimo número de la serie de Fibonacci de manera recursiva"""
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def print_fibonacci_sequence(count):
    """
    Imprime la secuencia de Fibonacci hasta `count` términos, asegurándose de
    que `count` sea positivo.
    """
    if count <= 0:
        print("Ingrese un número positivo.")
    else:
        print("Fibonacci sequence:")
        for i in range(count):
            # print(fibonacci(i + 1), end=" ") # Sin incluir el cero "0" en la serie
            print(fibonacci(i), end=" ") # Incluyendo el cero "0" en la serie
        print('')

# Solicita número de términos para serie Fibonacci y llama a la función para imprimirla.
num = int(input("Ingrese el número de términos para la serie Fibonacci: "))
print_fibonacci_sequence(num)
