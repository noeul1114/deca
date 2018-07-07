from django.shortcuts import render

from django.http.response import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user, login, logout

from django.utils import timezone

from django.shortcuts import get_object_or_404

from .models import Article

# Create your views here.

def board_index(request):
    user = get_user(request)
    article_list = Article.objects.all()
    if user.is_authenticated :
        return render(request, 'boards/board_index.html', {'user': user,
                                                           'article_list': article_list})
    else:
        return render(request, 'boards/board_index.html', {'article_list': article_list})

def board_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,
                            username=username,
                            password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('boards:board_index'))
        else:
            return render(request, 'boards/board_login.html')
    else:
        return render(request, 'boards/board_login.html')

def board_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('boards:board_index'))


def board_register(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(username=request.POST['username'],
                                            email=request.POST['email'],
                                            password=request.POST['password'],
                                            first_name=request.POST['first_name'],
                                            last_name=request.POST['last_name'])
            return HttpResponseRedirect(reverse('boards:board_index'))
        except:
            return render(request, 'boards/board_register.html', { 'error_message': '가입에 실패하였습니다.'})
    else:
        return  render(request, 'boards/board_register.html')


def board_write(request):
    user = get_user(request)
    if user.is_authenticated:
        if request.method == 'POST':
            A = Article(title=request.POST['title'],
                        article_text=request.POST['article_text'],
                        created_at=timezone.now(),
                        writer=user,
                        )
            try:
                A.save()
                return HttpResponseRedirect(reverse('boards:board_index'))
            except:
                return HttpResponseRedirect(reverse('boards:board_write'))

        return render(request, 'boards/board_write.html')
    else:
        return HttpResponseRedirect(reverse('boards:board_index'))


def board_delete(request):
    try:
        A = Article.objects.get(pk=request.POST['article_id'])
        A.delete()
        return HttpResponseRedirect(reverse('boards:board_index'))
    except:
        return HttpResponseRedirect(reverse('boards:board_index'))
