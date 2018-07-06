from django.shortcuts import render

from django.http.response import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.

def board_index(request):
    return render(request, 'boards/board_index.html', {'user': User.objects.filter(pk=3),
                                                       })

def board_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,
                            username=username,
                            password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('boards:board_index'), {'id': user.id})
        else:
            return render(request, 'boards/board_login.html')
    else:
        return render(request, 'boards/board_login.html')

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