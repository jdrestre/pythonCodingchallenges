"""Script para imprimir el triangulo de Pascal"""


def print_pascals_triangle(n):
    """
    The function `print_pascals_triangle` generates and prints Pascal's triangle up
    to a specified number of rows.
    """

    triangle = [[1]]
    for i in range(1, n):
        previous_row = triangle[-1]
        current_row = [1]
        for j in range(1, len(previous_row)):
            current_row.append(previous_row[j - 1] + previous_row[j])

        current_row.append(1)
        triangle.append(current_row)
    for row in triangle:
        print(" " * (n - len(row)), " ".join(map(str, row)))


rows = int(input("Ingrese el número de filas: "))
print_pascals_triangle(rows)
