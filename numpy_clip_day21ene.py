"""
numpy.clip se utiliza para limitar los valores de un array dentro de un rango específico
Toma tres argumentos:
- El array de entrada
- El valor mínimo
- El valor máximo

Para cada elemento del array:
- Si el elemento es menor que el valor mínimo, se reemplaza por el valor mínimo.
- Si el elemento es mayor que el valor máximo, se reemplaza por el valor máximo.
- Si el elemento está dentro del rango, se deja sin cambios.
"""
import numpy as np
arr = np.array([1, 2, 3, 4])
print(np.clip(arr, 2, 3))
