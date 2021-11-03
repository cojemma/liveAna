from django.shortcuts import render

# Create your views here.
def Home(requests):
    return render(requests, 'index.html')