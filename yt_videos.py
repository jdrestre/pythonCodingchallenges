"""
Descargador Simple de Videos de YouTube
Ejecución directa desde terminal
"""

import yt_dlp
from pathlib import Path


class YouTubeDownloader:
    """Descargador de videos de YouTube con selección de calidad"""

    def __init__(self, download_path="downloads"):
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)

    def progress_hook(self, d):
        """Muestra el progreso de descarga"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            print(f'\rDescargando: {percent} | Velocidad: {speed}', end='')
        elif d['status'] == 'finished':
            print('\n✓ Descarga completada. Procesando...')

    def get_available_formats(self, url):
        """
        Obtiene los 3 mejores formatos disponibles

        Returns:
            list: Lista de diccionarios con información de formatos
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                # Filtrar formatos que tienen video y audio
                formats = []
                for f in info.get('formats', []):
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        height = f.get('height', 0)
                        if height:
                            formats.append({
                                'format_id': f.get('format_id'),
                                'height': height,
                                'ext': f.get('ext', 'mp4'),
                                'filesize': f.get('filesize', 0),
                                'fps': f.get('fps', 0)
                            })

                # Ordenar por altura (resolución) de mayor a menor
                formats.sort(key=lambda x: x['height'], reverse=True)

                # Eliminar duplicados de misma resolución, mantener el primero (mejor)
                seen_heights = set()
                unique_formats = []
                for fmt in formats:
                    if fmt['height'] not in seen_heights:
                        seen_heights.add(fmt['height'])
                        unique_formats.append(fmt)

                # Retornar los 3 mejores formatos
                return unique_formats[:3]

        except Exception as e:
            print(f"❌ Error al obtener formatos: {e}")
            return []

    def download_video(self, url, format_choice=None):
        """
        Descarga un video de YouTube

        Args:
            url: URL del video
            format_choice: ID del formato seleccionado, o None para mejor calidad
        """

        ydl_opts = {
            'outtmpl': str(self.download_path / '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'merge_output_format': 'mp4',
        }

        if format_choice:
            # Descargar formato específico + mejor audio disponible
            ydl_opts['format'] = f'{format_choice}+bestaudio/best'
        else:
            # Mejor calidad disponible
            ydl_opts['format'] = 'bestvideo+bestaudio/best'

        try:
            print(f"\n📂 Guardando en: {self.download_path.absolute()}\n")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            print("\n✅ ¡Descarga exitosa!")
            return True

        except Exception as e:
            print(f"\n❌ Error: {e}")
            return False


def format_filesize(size):
    """Convierte bytes a formato legible"""
    if not size:
        return "Desconocido"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def main():
    """Función principal"""
    downloader = YouTubeDownloader()

    print("\n" + "="*60)
    print("  DESCARGADOR DE YOUTUBE")
    print("="*60)

    url = input("\n📎 Ingresa la URL del video: ").strip()

    if not url:
        print("❌ URL vacía")
        return

    print("\n🔍 Obteniendo formatos disponibles...")
    formats = downloader.get_available_formats(url)

    if not formats:
        print("\n⚠️  No se pudieron obtener formatos. Descargando en mejor calidad...")
        downloader.download_video(url)
        return

    print("\n📊 Formatos disponibles:\n")
    print("-"*60)

    for i, fmt in enumerate(formats, 1):
        resolution = f"{fmt['height']}p"
        fps = f"{fmt['fps']}fps" if fmt['fps'] else ""
        size = format_filesize(fmt['filesize'])

        print(
            f"{i}. {resolution:>6} {fps:>6} | Tamaño: {size:>12} | Formato: {fmt['ext']}")

    print("-"*60)

    choice = input(
        f"\nSelecciona formato (1-{len(formats)}) [Enter para opción 1]: ").strip()

    if not choice:
        choice = '1'

    try:
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(formats):
            selected = formats[choice_idx]
            print(f"\n🎬 Descargando en {selected['height']}p...")
            downloader.download_video(url, selected['format_id'])
        else:
            print("\n⚠️  Opción inválida. Descargando mejor calidad...")
            downloader.download_video(url)
    except ValueError:
        print("\n⚠️  Entrada inválida. Descargando mejor calidad...")
        downloader.download_video(url)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
