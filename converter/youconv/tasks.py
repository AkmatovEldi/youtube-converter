import youtube_dl
from urllib.parse import quote
from converter.celery import app
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template, render_to_string

User = get_user_model()


@app.task
def converting_send_massage(link, user_email, user_id, hostname):
    from youconv.models import History

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
            info_dict = ydl.extract_info(link, download=False)
            video_title = info_dict.get('title', None)
            video_title += '.mp3'
            ydl.download([link])
            user = User.objects.get(id=user_id)
            History.objects.create(url=link, user=user, file_name=video_title)
            url = hostname + 'media/' + quote(video_title)
            content = render_to_string('youconv/message.html') + url
            send_message = EmailMessage('Конвертирование', content, to=[user_email])
            send_message.send()
    except:
        pass
