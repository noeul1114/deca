from django import forms

from django_summernote.widgets import SummernoteWidget


class BasicForm(forms.Form):
    title = forms.CharField(max_length=200)
    article_text = forms.CharField(widget=SummernoteWidget())

    def __init__(self, *args, **kwargs):
        # Get 'initial' argument if any
        initial_arguments = kwargs.get('initial', None)
        updated_initial = {}
        if initial_arguments:
            updated_initial['title'] = initial_arguments.get('title', None)
            updated_initial['article_text'] = initial_arguments.get('article_text', None)
        # You can also initialize form fields with hardcoded values
        # or perform complex DB logic here to then perform initialization
        updated_initial['comment'] = 'Please provide a comment'
        # Finally update the kwargs initial reference
        kwargs.update(initial=updated_initial)
        super(BasicForm, self).__init__(*args, **kwargs)
