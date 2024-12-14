"""reproducir videos de Youtube utilizando python"""

import yt_dlp
import subprocess

def search_youtube(query):
    ydl_opts = {
        'default_search': 'ytsearch',
        'max_downloads': 1,
        'noplaylist': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(query, download=False)
        video_url = result['entries'][0]['webpage_url']
        return video_url

def open_in_browser(url):
    # Usar el comando de Windows para abrir el navegador desde WSL
    subprocess.run(['cmd.exe', '/c', 'start', 'msedge', url], check=True)

query = input("Ingresa el nombre de la canción: ")
video_url = search_youtube(query)
open_in_browser(video_url)


# import webbrowser
# from yt_dlp import YoutubeDL


# def search_youtube(query):
#     with YoutubeDL({'quiet': True}) as ydl:
#         result = ydl.extract_info(f"ytsearch:{query}", download=False)[
#             'entries'][0]
#         return result['webpage_url']


# # Solicita al usuario que introduzca el nombre de la canción
# song_name = input("Introduce el nombre de la canción: ")

# # Busca y muestra los primeros 10 resultados
# # search_youtube(song_name)

# # Busca el video en YouTube
# video_url = search_youtube(song_name)

# # Abre el video en el navegador predeterminado
# webbrowser.open(video_url)
