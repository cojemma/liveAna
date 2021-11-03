import requests
from django.shortcuts import render
from .utils import get_title, chat_record, wExcel

# Create your views here.
def Home(request):
    if request.method == 'POST':
        url = request.POST.get('video_url')
        try:
            title = get_title(url)
        except:
            print("Url Error")
            return render(request, 'index.html')
        if title != None:
            request.session['url'] = url
            request.session['title'] = title
            print(request.session['url'], request.session['title'])
    return render(request, 'index.html')