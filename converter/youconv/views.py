import os

from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import render, redirect
from .forms import UrlForm
import youtube_dl
import io
from django.http import FileResponse
from .models import History


def get_status(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def redirect_by_link(request):
    link = UrlForm()
    if request.method == 'POST':
        link = UrlForm(request.POST)
        if link.is_valid():
            url = link.cleaned_data['address']
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [get_status],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            file_path = os.path.join('/home/eldi/working/intership/2Task/youtube-converter/converter/', 'test.mp3')
            History.objects.create(url=url, user=User.objects.first())
            return FileResponse(open(file_path, 'rb'))

    return render(request, 'youconv/converter.html', {'link': link})