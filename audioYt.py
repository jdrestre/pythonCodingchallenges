from pytube import YouTube

url = input('Enter a Video to Download Audio: ')
yt = YouTube(url)

# Filter audio streams and download the first one
audio_stream = yt.streams.filter(only_audio=True).first()
audio_stream.download()
