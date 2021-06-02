from django import forms


class UrlForm(forms.Form):
    address = forms.URLField()
