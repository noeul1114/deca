from django.shortcuts import render

from django.http.response import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user, login, logout

from django.utils import timezone

from django.shortcuts import get_object_or_404

from .models import Article, Comment

# Create your views here.


def board_index(request):
    user = get_user(request)
    article_list = Article.objects.all()
    if user.is_authenticated :
        return render(request, 'boards/board_index.html', {'user': user,
                                                           'article_list': article_list})
    else:
        return render(request, 'boards/board_index.html', {'article_list': article_list})


def board_index_name(request, board_url='blueboard'):
    user = get_user(request)
    article_list = Article.objects.filter(board_name__url=board_url)
    if user.is_authenticated :
        return render(request, 'boards/board_index.html', {'user': user,
                                                           'article_list': article_list,
                                                           })
    else:
        return render(request, 'boards/board_index.html', {'article_list': article_list})


def board_detail(request, article_id):
    article_list = Article.objects.all()
    A = get_object_or_404(Article, pk=article_id)
    C = Comment.objects.filter(article_id=article_id)
    return render(request, 'boards/board_detail.html', {'article_detail': A,
                                                        'article_list': article_list,
                                                        'comment_list': C})


def board_vote(request, article_id):
    A = get_object_or_404(Article, pk=article_id)
    if request.POST['vote'] == 'up':
        A.upvote += 1
        A.save()
        return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': article_id}))
    if request.POST['vote'] == 'down':
        A.downvote += 1
        A.save()
        return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': article_id}))
    # up이랑 down 이랑 안되는 케이스도 어떻게 커버하는게 좋을듯



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
            User.objects.create_user(username=request.POST['username'],
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


def board_edit(request):
    if request.method == "POST":
        user = get_user(request)
        A = get_object_or_404(Article, pk=request.POST['article_id'])
        if user.is_authenticated:
            if A.writer_id == user.id:
                return render(request, 'boards/board_edit.html', {'article_edit': A})
            else:
                return HttpResponseRedirect(reverse('boards:board_index'))
        else:
            return HttpResponseRedirect(reverse('boards:board_index'))
    else:
        return HttpResponseRedirect(reverse('boards:board_index'))


def board_edit_fix(request):
    if request.method == "POST":
        user = get_user(request)
        A = get_object_or_404(Article, pk=request.POST['article_id'])
        if user.is_authenticated:
            if A.writer_id == user.id:
                try:
                    A.article_text = request.POST['article_text']
                    A.title = request.POST['title']
                    A.edited_at = timezone.now()
                    A.save()
                    return HttpResponseRedirect(reverse('boards:board_index'))
                except:
                    return HttpResponseRedirect(reverse('boards:board_edit'))
            else:
                return HttpResponseRedirect(reverse('boards:board_index'))
        else:
            return HttpResponseRedirect(reverse('boards:board_index'))
    else:
        return HttpResponseRedirect(reverse('boards:board_index'))


def board_delete(request):
    try:
        A = get_object_or_404(Article, pk=request.POST['article_id'])
        A.delete()
        return HttpResponseRedirect(reverse('boards:board_index'))
    except:
        return HttpResponseRedirect(reverse('boards:board_index'))


def board_comment_write(request):
    user = get_user(request)
    article = Article.objects.get(pk=request.POST['article_id'])
    if user.is_authenticated:
        if request.method == 'POST':
            try:
                C = Comment(comment_text=request.POST['comment_text'],
                            created_at=timezone.now(),
                            edited_at=timezone.now(),
                            writer_id=user.id,
                            article_id=article.id,
                            )
                C.save()
                return HttpResponseRedirect(
                    reverse('boards:board_detail', kwargs={'article_id': request.POST['article_id']}))
            except:
                return HttpResponseRedirect(
                    reverse('boards:board_detail', kwargs={'article_id': request.POST['article_id']}))
        else:
            return HttpResponseRedirect(
                reverse('boards:board_detail', kwargs={'article_id': request.POST['article_id']}))
    else:
        return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': request.POST['article_id']}))


def board_comment_vote(request, comment_id):
    C = get_object_or_404(Comment, pk=comment_id)
    if request.POST['vote'] == 'up':
        C.upvote += 1
        C.save()
        return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': C.article_id}))
    if request.POST['vote'] == 'down':
        C.downvote += 1
        C.save()
        return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': C.article_id}))
    # up이랑 down 이랑 안되는 케이스도 어떻게 커버하는게 좋을듯

