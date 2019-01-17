from django import forms

from django_summernote.widgets import SummernoteWidget
from .models import Board

from phonenumber_field.formfields import PhoneNumberField


class BasicForm(forms.Form):
    title = forms.CharField(max_length=200)
    project = forms.ModelChoiceField(queryset=Board.objects.filter(has_higher_board=False, activated=True))
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


class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label='아이디', required=True, min_length=10)
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='비밀번호', min_length=8)


class UserRegisterFormOptional(forms.Form):
    CHOICES = (('M', '남자',), ('W', '여자',))

    profile_image = forms.ImageField(label='프로필 이미지', required=False)

    nickname = forms.CharField(max_length=30, label='닉네임', required=False)

    family_name = forms.CharField(max_length=150, label='성', required=False)
    first_name = forms.CharField(max_length=30, label='이름', required=False)

    email = forms.EmailField(max_length=200, label='이메일', required=False)

    age = forms.IntegerField(min_value=0, max_value=255, label='나이', required=False)
    sex = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='성별', required=False)

    phone = PhoneNumberField(label='전화번호', required=False)

    introduction = forms.CharField(max_length=400, widget=forms.Textarea, label='소개글', required=False)
