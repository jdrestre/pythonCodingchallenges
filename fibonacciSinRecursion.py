def fibonacci_series(n):
    """Calcula los n términos de la serie Fibonacci y los guarda en una lista"""
    a, b = 0, 1
    series = []
    for _ in range(n):
        series.append(a)
        a, b = b, a + b
    return series

num_terms = int(input("Ingrese número de términos: "))
if num_terms <= 0:
    print("Por favor ingrese un entero positivo.")
else:
    print("Serie Fibonacci sin `recursion`:")
    print(fibonacci_series(num_terms))
