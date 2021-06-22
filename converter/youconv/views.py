import os

from django.contrib.auth.models import User
from django.http import Http404
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
    form = UrlForm()
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['address']
            user_email = form.cleaned_data['user_email']
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': './media/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [get_status],
            }
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    video_title = info_dict.get('title', None)
                    video_title += '.mp3'
                    ydl.download([url])
            except:
                raise Http404()

            History.objects.create(url=url, user=request.user, file_name=video_title)

    return render(request, 'youconv/converter.html', {'form': form})


def get_history(request):
    histories = History.objects.filter(user=request.user, file_name__isnull=False)
    return render(request, 'youconv/history.html', {'histories': histories})


def get_history_details(request, history_id):
    history = History.objects.get(id=history_id)
    return render(request, 'youconv/history_details.html', {'history': history})
