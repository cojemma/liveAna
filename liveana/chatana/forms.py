from django import forms

class UrlForm(forms.Form):
    video_url = forms.CharField(label='url', max_length=200)
