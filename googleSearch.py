from googlesearch import search
query = input("Pregunta cualquier cosa: ")

for url in search(query):
    print(url)
