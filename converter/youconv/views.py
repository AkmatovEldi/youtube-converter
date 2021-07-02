from django.shortcuts import render, redirect
from .forms import UrlForm
from .models import History
from youconv.tasks import converting_send_massage


def redirect_by_link(request):
    form = UrlForm()
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['address']
            user_email = form.cleaned_data['user_email']
            converting_send_massage.delay(url, user_email, request.user.id, request.build_absolute_uri())
            return render(request, 'youconv/successful.html', {'user_email': user_email}) 
    return render(request, 'youconv/converter.html', {'form': form})


def get_history(request):
    histories = History.objects.filter(user=request.user, file_name__isnull=False)
    return render(request, 'youconv/history.html', {'histories': histories})


def get_history_details(request, history_id):
    return render(request, 'youconv/history_details.html', {'history': History.objects.get(id=history_id)})
