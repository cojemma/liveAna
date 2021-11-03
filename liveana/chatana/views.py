import requests
from django.shortcuts import render
from .utils import get_title, chat_record, wExcel

# Create your views here.


def home(request):
    if request.method == 'POST':
        url = request.POST.get('video_url')
        try:
            title = get_title(url)
        except ValueError:
            print("Url Error")
            return render(request, 'index.html')
        if title:
            request.session['url'] = url
            request.session['title'] = title
            print(request.session['url'], request.session['title'])
    return render(request, 'index.html')
