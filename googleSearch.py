"""
Realizar búsqueda en Google utilizando python con el módulo googlesearch
"""
from googlesearch import search
query = input("Pregunta cualquier cosa: ")

for index, url in enumerate(search(query)):
    if index < 10:
        print(url)
    else:
        break
