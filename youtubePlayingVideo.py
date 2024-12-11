"""reproducir videos de Youtube utilizando python"""

import webbrowser
from yt_dlp import YoutubeDL


def search_youtube(query):
    with YoutubeDL({'quiet': True}) as ydl:
        result = ydl.extract_info(f"ytsearch:{query}", download=False)[
            'entries'][0]
        return result['webpage_url']


# Solicita al usuario que introduzca el nombre de la canción
song_name = input("Introduce el nombre de la canción: ")

# Busca y muestra los primeros 10 resultados
# search_youtube(song_name)

# Busca el video en YouTube
video_url = search_youtube(song_name)

# Abre el video en el navegador predeterminado
webbrowser.open(video_url)
