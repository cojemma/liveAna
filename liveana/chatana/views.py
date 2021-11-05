import requests
from django.shortcuts import render, redirect
from .utils import get_title, chat_record, wExcel, get_stream
from django.http import HttpResponse
from django.contrib import messages
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
            return redirect('download/')
    return render(request, 'index.html')

def download(request):
    if request.session.get('url') == None or request.session.get('title') == None:
        return redirect('')
    title = request.session['title']
    url = request.session['url']
    try:
        data = chat_record(url)
    except:
        messages.warning(request, '連結錯誤，請重試。')
        request.session.flush()
        return redirect('/')
    #print(data)
    excel = wExcel(data, title)
    excel_stream = get_stream(excel)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="chat-analyze.xlsx"'
    response.write(excel_stream)
    request.session.flush()
    return response
