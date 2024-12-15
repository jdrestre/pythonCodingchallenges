    """Programa para buscar números de fibonacci utilizando recursion"""


def fibonacci(n):
    """Calcula el enésimo número de la serie de Fibonacci de manera recursiva"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)  # Aquí está la recursion


def print_fibonacci_sequence(count):
    """
    Imprime la secuencia de Fibonacci hasta `count` términos, asegurándose de
    que `count` sea positivo.
    """
    if count <= 0:
        print("Ingrese un número positivo.")
    else:
        print("Serie Fibonacci con `recursion`:")
        for i in range(count):
            # print(fibonacci(i + 1), end=" ") # Sin incluir el "0" en la serie
            print(fibonacci(i), end=" ")  # Incluyendo el "0" en la serie
        print('')


# Ingresa términos para serie Fibonacci y llama la función para imprimirla.
num = int(input("Ingrese el número de términos para la serie Fibonacci: "))
print_fibonacci_sequence(num)
