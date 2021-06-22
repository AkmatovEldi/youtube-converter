import youtube_dl
from converter.celery import app



@app.task
def hello(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': './media/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
    except:
        pass

