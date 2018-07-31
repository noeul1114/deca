from django.shortcuts import render

from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user, login, logout

from django.utils import timezone

from django.shortcuts import get_object_or_404

from .models import Article, Comment, Vote
from django_summernote.models import Attachment
from .form import BasicForm




def board_index(request):
    user = get_user(request)
    article_list = Article.objects.filter(published=True, activated=True).order_by('upvote').reverse()

    if user.is_authenticated :
        return render(request, 'boards/board_index.html', {'user': user,
                                                           'article_list': article_list})
    else:
        return render(request, 'boards/board_index.html', {'article_list': article_list})


def board_index_name(request, board_url='blueboard'):
    user = get_user(request)
    article_list = Article.objects.filter(board_name__url=board_url, published=True, activated=True)
    if user.is_authenticated :
        return render(request, 'boards/board_index.html', {'user': user,
                                                           'article_list': article_list,
                                                           })
    else:
        return render(request, 'boards/board_index.html', {'article_list': article_list})


def board_detail(request, article_id):
    user = get_user(request)
    if user.is_authenticated:
        article_list = Article.objects.filter(published=True, activated=True).order_by('upvote').reverse()
        A = get_object_or_404(Article, pk=article_id)
        C = Comment.objects.filter(article_id=article_id)
        return render(request, 'boards/board_detail.html', {'article_detail': A,
                                                            'user': user,
                                                            'article_list': article_list,
                                                            'comment_list': C})
    else:
        article_list = Article.objects.filter(published=True, activated=True).order_by('upvote').reverse()
        A = get_object_or_404(Article, pk=article_id)
        C = Comment.objects.filter(article_id=article_id)
        return render(request, 'boards/board_detail.html', {'article_detail': A,
                                                            'article_list': article_list,
                                                            'comment_list': C})


def board_vote(request, article_id):
    A = get_object_or_404(Article, pk=article_id)
    user = get_user(request)
    if request.method == 'POST':
        if request.POST['vote'] == 'up':
            A.upvote += 1
            A.save()
            return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': article_id}))
        if request.POST['vote'] == 'down':
            A.downvote += 1
            A.save()
            return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': article_id}))
        # up이랑 down 이랑 안되는 케이스도 어떻게 커버하는게 좋을듯
    elif request.method == 'GET':
        if request.GET['vote'] == 'up':
            A.upvote += 1
            A.save()
            return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': article_id}))
        if request.GET['vote'] == 'down':
            A.downvote += 1
            A.save()
            return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': article_id}))
    else:
        return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': article_id}))


def board_login(request):
    user = get_user(request)
    if user.is_authenticated:
        article_list = Article.objects.filter(published=True, activated=True).order_by('upvote').reverse()
        return render(request, 'boards/board_index.html', {'user': user,
                                                           'article_list': article_list,
                                                           'error_message': '이미 로그인 되어있습니다'
                                                           })
    else:
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
                return render(request, 'boards/board_login.html', {'error_message': '아이디 혹은 비밀번호가 틀립니다.'})
        else:
            return render(request, 'boards/board_login.html')


def board_logout(request):
    user = get_user(request)
    if user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('boards:board_index'))
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
        return render(request, 'boards/board_register.html')


def board_write(request):
    user = get_user(request)
    if user.is_authenticated:
        if Article.objects.filter(writer=user, published=False).count() == 0:
            A = Article.objects.create(title='',
                                       article_text='',
                                       created_at=timezone.now(),
                                       writer=user,
                                       )
        else:
            A = get_object_or_404(Article, writer=user, published=False)

        if request.method == 'POST':
            A.title = request.POST['title']
            A.article_text = request.POST['article_text']
            A.created_at = timezone.now()
            A.writer = user
            try:
                A.published = True
                A.activated = True
                A.save()
                return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': A.id}))
            except:
                form = BasicForm()
                return render(request, 'boards/board_write.html', {'form': form,
                                                                   })
        else:
            form = BasicForm()
            return render(request, 'boards/board_write.html', {'form': form,
                                                               })
    else:
        article_list = Article.objects.filter(published=True, activated=True).order_by('upvote').reverse()
        return render(request, 'boards/board_index.html', {'user': user,
                                                           'article_list': article_list,
                                                           'error_message': '글을 쓰기 위해선 로그인 해주세요!'
                                                           })

# def board_write(request):
#     user = get_user(request)
#     if user.is_authenticated:
#         if request.method == 'POST':
#             A = Article(title=request.POST['title'],
#                         article_text=request.POST['article_text'],
#                         created_at=timezone.now(),
#                         writer=user,
#                         )
#             try:
#                 A.save()
#                 return HttpResponseRedirect(reverse('boards:board_index'))
#             except:
#                 return HttpResponseRedirect(reverse('boards:board_write'))
#
#         return render(request, 'boards/board_write.html')
#     else:
#         return HttpResponseRedirect(reverse('boards:board_index'))


def board_delete(request, article_id):
    user = get_user(request)
    A = get_object_or_404(Article, pk=article_id)
    if user.is_authenticated:
        if user == A.writer:
            return render(request, 'boards/board_delete.html', {'user' : user,
                                                                'article': A,
                                                                })
        else:
            article_list = Article.objects.all()
            C = Comment.objects.filter(article_id=article_id)
            return render(request, 'boards/board_detail.html', {'article_detail': A,
                                                                'article_list': article_list,
                                                                'comment_list': C,
                                                                'error_message': "잘못된 접근입니다."})
    else:
        article_list = Article.objects.all()
        C = Comment.objects.filter(article_id=article_id)
        return render(request, 'boards/board_detail.html', {'article_detail': A,
                                                            'article_list': article_list,
                                                            'comment_list': C,
                                                            'error_message': "잘못된 접근입니다."})


def board_delete_fix(request):
    user = get_user(request)
    A = get_object_or_404(Article, pk=request.POST['article_id'])
    if user.is_authenticated:
        if user == A.writer:
            try:
                A.activated = False
                A.save()
                return HttpResponseRedirect(reverse('boards:board_index'))
            except:
                article_list = Article.objects.filter(published=True, activated=True).order_by('upvote').reverse()
                C = Comment.objects.filter(article_id=request.POST['article_id'])
                return render(request, 'boards/board_detail.html', {'article_detail': A,
                                                                    'article_list': article_list,
                                                                    'comment_list': C,
                                                                    'error_message': "잘못된 접근입니다."})
        else:
            article_list = Article.objects.all()
        C = Comment.objects.filter(article_id=request.POST['article_id'])
        return render(request, 'boards/board_detail.html', {'article_detail': A,
                                                            'article_list': article_list,
                                                            'comment_list': C,
                                                            'error_message': "잘못된 접근입니다."})
    else:
        article_list = Article.objects.all()
        C = Comment.objects.filter(article_id=request.POST['article_id'])
        return render(request, 'boards/board_detail.html', {'article_detail': A,
                                                            'article_list': article_list,
                                                            'comment_list': C,
                                                            'error_message': "잘못된 접근입니다."})

def board_edit(request, article_id):
    user = get_user(request)
    A = get_object_or_404(Article, pk=article_id)
    if request.method == "GET":
        if user.is_authenticated:
            if A.writer_id == user.id:
                return render(request, 'boards/board_edit.html', {'article_edit': A})
            else:
                article_list = Article.objects.filter(published=True, activated=True).order_by('upvote').reverse()
                C = Comment.objects.filter(article_id=article_id)
                return render(request, 'boards/board_detail.html', {'article_detail': A,
                                                                    'article_list': article_list,
                                                                    'comment_list': C,
                                                                    'error_message': "잘못된 접근입니다."})
        else:
            article_list = Article.objects.filter(published=True, activated=True).order_by('upvote').reverse()
            C = Comment.objects.filter(article_id=article_id)
            return render(request, 'boards/board_detail.html', {'article_detail': A,
                                                                'article_list': article_list,
                                                                'comment_list': C,
                                                                'error_message': "잘못된 접근입니다."})
    else:
        article_list = Article.objects.filter(published=True, activated=True).order_by('upvote').reverse()
        C = Comment.objects.filter(article_id=article_id)
        return render(request, 'boards/board_detail.html', {'article_detail': A,
                                                            'article_list': article_list,
                                                            'comment_list': C,
                                                            'error_message': "잘못된 접근입니다."})


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
                article.comment_count += 1

                C.save()
                article.save()
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

