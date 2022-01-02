import requests
from django.shortcuts import render, redirect
from .utils import get_title, chat_record, wExcel, get_stream
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
# Create your views here.


class Views:

    def home(request):
        request.session.flush()
        print(request.session.get('title'))
        if request.method == 'POST':
            url = request.POST.get('video_url')
            try:
                title = get_title(url)
            except ValueError:
                print("Url Error")
                messages.warning(request, '連結錯誤，請重試。')
                request.session.flush()
                return redirect('/')
            if title:
                request.session['url'] = url
                request.session['title'] = title
                print(request.session['url'], request.session['title'])
                return redirect('download/')
        return render(request, 'index.html')

    def download(request):
        if not(request.session.get('url') and request.session.get('title')):
            return redirect('')
        title = request.session['title']
        url = request.session['url']
        try:
            data = chat_record(url)
        except ValueError:
            messages.warning(request, '連結錯誤，請重試。')
            request.session.flush()
            return redirect('/')
        #print(data)
        excel = wExcel(data, title)
        excel_stream = get_stream(excel)
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="chat-analyze.xlsx"'
        response.write(excel_stream)
        print(request.session['url'], request.session['title'])
        return response

    def download_info(request):
        title = request.session.get('title')
        if not title:
            data = {
                'info': '準備下載...'
            }
        else:
            data = {
                'info': f'準備下載{title}的留言統計...',
            }
        return JsonResponse(data)
