"""
Asignación de expresiones: Operador walrus (:=) Permite asignar valores a variables como parte de una expresión
Asignación de tuples: permite asignar múltiples valores a múltiples variables en una sola línea
"""

(a := 6, 9)  # Solo asigna valor a 'a', el 9 no se asigna a nada
(a, b := 16, 19)  # Error sintaxis, solo está asignando 16 a 'b' (a := 16, b := 19)
print(f"{a=} {b=}")
print(a + b)

if (c := 6):
    print(f"c ha sido asignado a {c}")

if (d := 9) > 0:
    print(f"d ha sido asignado a {d}")

print(f"La Suma de c y d es: {c} + {d} =", c + d)
