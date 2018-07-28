from django import forms

from django_summernote.widgets import SummernoteWidget


class BasicForm(forms.Form):
    title = forms.CharField(max_length=200)
    article_text = forms.CharField(widget=SummernoteWidget())
