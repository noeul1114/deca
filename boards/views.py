from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from datetime import timedelta

from django.db.models import F

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user, login, logout

from django.views.generic import TemplateView

from django.utils import timezone

from django.shortcuts import get_object_or_404, Http404

from django.conf import settings

from .models import Article, ArticleIpLog, Comment, CommentIpLog, Board
from .models import Attachment, Board, AdditionalUserProfile, BoardImage, UserProfileImage
from .form import BasicForm, UserRegisterForm, UserRegisterFormOptional

from bs4 import BeautifulSoup


class assetlink(TemplateView):
    template_name = "boards/assetlinks.json"
    content_type = "application/json"


def board_index(request):
    user = get_user(request)
    article_list_top = Article.objects.filter(published=True, activated=True, created_at__gte=timezone.now() - timedelta(days=3)).order_by('upvote').reverse()[:8]
    article_list = Article.objects.filter(published=True, activated=True).reverse()

    template = 'boards/board_index.html'
    page_fragment = 'boards/board_index_fragment.html'

    if request.is_ajax():
        template = page_fragment

    if user.is_authenticated :
        return render(request, template, {'user': user,
                                          'page_fragment': page_fragment,
                                          'article_list': article_list,
                                          'article_list_top': article_list_top})
    else:
        return render(request, template, {'article_list': article_list,
                                          'page_fragment': page_fragment,
                                          'article_list_top': article_list_top})


def board_index_name(request, board_id):
    user = get_user(request)
    board = get_object_or_404(Board, pk=board_id)
    article_list_top = Article.objects.filter(board_id=board_id, published=True, activated=True, created_at__gte=timezone.now() - timedelta(days=3)).order_by('upvote').reverse()[:8]
    article_list = Article.objects.filter(board_id=board_id, published=True, activated=True).reverse()

    template = 'boards/board_index.html'
    page_fragment = 'boards/board_index_fragment.html'

    if request.is_ajax():
        template = page_fragment

    if user.is_authenticated :
        return render(request, template, {'user': user,
                                          'board': board,
                                          'page_fragment': page_fragment,
                                          'article_list': article_list,
                                          'article_list_top': article_list_top})
    else:
        return render(request, template, {'article_list': article_list,
                                          'board': board,
                                          'page_fragment': page_fragment,
                                          'article_list_top': article_list_top})


# def board_index_name(request, board_url=''):
#     user = get_user(request)
#     article_list = Article.objects.filter(board_name__url=board_url, published=True, activated=True)
#     if user.is_authenticated :
#         return render(request, 'boards/board_index.html', {'user': user,
#                                                            'article_list': article_list,
#                                                            })
#     else:
#         return render(request, 'boards/board_index.html', {'article_list': article_list})


def board_detail(request, article_id):
    user = get_user(request)
    A = get_object_or_404(Article, pk=article_id)
    if A.published and A.activated:
        if user.is_authenticated:
            # article_list = Article.objects.filter(published=True, activated=True).order_by('upvote').reverse()
            C = Comment.objects.filter(article_id=article_id)
            A.hit += 1
            A.save()
            return render(request, 'boards/board_detail.html', {'article_detail': A,
                                                                'user': user,
                                                                'comment_list': C})
        else:
            # article_list = Article.objects.filter(published=True, activated=True).order_by('upvote').reverse()
            C = Comment.objects.filter(article_id=article_id)
            A.hit += 1
            A.save()
            return render(request, 'boards/board_detail.html', {'article_detail': A,
                                                                'comment_list': C})
    else:
        return Http404()
        # article_list_top = Article.objects.filter(published=True, activated=True,
        #                                           created_at__gte=timezone.now() - timedelta(days=3)).order_by(
        #     'upvote').reverse()[:8]
        # article_list = Article.objects.filter(published=True, activated=True).reverse()
        #
        # if user.is_authenticated:
        #     return render(request, 'boards/board_index.html', {'user': user,
        #                                                        'article_list': article_list,
        #                                                        'article_list_top': article_list_top,
        #                                                        'error_message': '볼 수 없는 게시물입니다.'})
        # else:
        #     return render(request, 'boards/board_index.html', {'article_list': article_list,
        #                                                        'article_list_top': article_list_top,
        #                                                        'error_message': '볼 수 없는 게시물입니다.'})


def board_vote(request, article_id):
    A = get_object_or_404(Article, pk=article_id)
    user = get_user(request)
    user_ip = get_client_ip(request)
    if ArticleIpLog.objects.filter(ip=user_ip, article=A).exists():
        return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': article_id}))
    else:
        if get_user(request).is_active:
            ArticleIpLog.objects.create(ip=user_ip,
                                        user=user,
                                        article=A,
                                        created_at=timezone.now())
        else:
            ArticleIpLog.objects.create(ip=user_ip,
                                        article=A,
                                        created_at=timezone.now())
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
        article_list_top = Article.objects.filter(published=True, activated=True,
                                                  created_at__gte=timezone.now() - timedelta(days=3)).order_by(
            'upvote').reverse()[:8]
        article_list = Article.objects.filter(published=True, activated=True).reverse()
        return render(request, 'boards/board_index.html', {'user': user,
                                                           'article_list': article_list,
                                                           'article_list_top': article_list_top,
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
        form_required = UserRegisterForm(data=request.POST)
        form_optional = UserRegisterFormOptional(data=request.POST)
        try:
            form_required.clean()
            user = User.objects.create_user(username=request.POST['username'],
                                            password=request.POST['password'],)
        except:
            return render(request, 'boards/board_register.html', {'form_required': form_required,
                                                              'form_optional': form_optional})

        if len(request.FILES) != 0:
            kwargs = request.POST.copy()
            file = request.FILES['profile_image']
            try:
                profile_image = UserProfileImage()

                kwargs = request.POST.copy()
                kwargs.pop("csrfmiddlewaretoken", None)
                kwargs.pop("username", None)
                kwargs.pop("introduction", None)
                kwargs.pop("age", None)
                kwargs.pop("sex", None)
                kwargs.pop("phone", None)
                kwargs.pop("email", None)
                kwargs.pop("family_name", None)
                kwargs.pop("first_name", None)
                kwargs.pop("password", None)
                kwargs.pop("nickname", None)

                profile_image = UserProfileImage()
                profile_image.file = file
                profile_image.name = file.name
                profile_image.user = user

                profile_image.save(**kwargs)

            except IOError:
                if user:
                    user.delete()
                if profile_image:
                    profile_image.delete()
                return render(request, 'boards/board_register.html', {'form_required': form_required,
                                                              'form_optional': form_optional})

        if form_optional.is_bound:
            try:
                register_user = get_object_or_404(User, username=request.POST['username'])
                register_user.first_name = request.POST['first_name']
                register_user.email = request.POST['email']
                register_user.last_name = request.POST['family_name']

                register_user.save()

                addtional = AdditionalUserProfile()
                addtional.nickname = request.POST['nickname']
                addtional.introduction = request.POST['introduction']
                if request.POST['age'] == '':
                    addtional.age = None
                else:
                    addtional.age = request.POST['age']
                addtional.sex = request.POST['sex']
                addtional.phone = request.POST['phone']
                addtional.user = user

                addtional.save()

                return HttpResponseRedirect(reverse('boards:board_index'))

            except:
                if user:
                    user.delete()
                if len(request.FILES) != 0:
                    profile_image.delete()
                return render(request, 'boards/board_register.html', {'form_required': form_required,
                                                                  'form_optional': form_optional})



    else:
        form_required = UserRegisterForm()
        form_optional = UserRegisterFormOptional()

        return render(request, 'boards/board_register.html', {'form_required': form_required,
                                                              'form_optional': form_optional})


def board_agreement(request):
    return render(request, 'boards/board_agreement.html')


def board_write(request, **kwargs):
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
            if request.POST['submit'] == 'True':
                A.title = request.POST['title']
                A.article_text = request.POST['article_text']
                A.created_at = timezone.now()
                A.writer = user

                soup = BeautifulSoup(A.article_text, "html.parser")

                if soup.img != None:
                    A.image = soup.img['src']
                else:
                    # 여기에 사진 없을경우 랜덤으로 붙여넣을 알고리즘 추가
                    pass

                try:
                    A.published = True
                    A.activated = True
                    A.board_id = request.POST['project']
                    A.save()
                    Attachment.objects.filter(article=A).update(activated=True)
                    return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': A.id}))
                except:
                    form = BasicForm(initial={'title': A.title,
                                              'article_text': A.article_text,
                                              })
                    return render(request, 'boards/board_write.html',
                                  {'form': form,
                                   'error_message': '글을 쓰는데에 실패했습니다. 다시 시도해주세요',
                                    })
            elif request.POST['submit'] == 'False':
                A.title = request.POST['title']
                A.article_text = request.POST['article_text']
                A.created_at = timezone.now()
                A.writer = user

                soup = BeautifulSoup(A.article_text, "html.parser")

                if soup.img != None:
                    A.image = soup.img['src']
                else:
                    # 여기에 사진 없을경우 랜덤으로 붙여넣을 알고리즘 추가
                    pass

                try:
                    A.save()
                    form = BasicForm(initial={'title': A.title,
                                              'article_text': A.article_text,
                                              })
                    return render(request, 'boards/board_write.html', {'form': form,
                                                                       'success_message': '글을 저장했습니다.',
                                                                       })
                except:
                    form = BasicForm(initial={'title': A.title,
                                              'article_text': A.article_text,
                                              })
                    return render(request, 'boards/board_write.html',
                                  {'form': form,
                                   'error_message': '글을 저장하는 데에 실패했습니다. 다시 시도해주세요',
                                    })
        else:
            form = BasicForm(initial={'title': A.title,
                                      'article_text': A.article_text,
                                      })
            return render(request, 'boards/board_write.html', {'form': form,
                                                               })
    else:
        article_list_top = Article.objects.filter(published=True, activated=True,
                                                  created_at__gte=timezone.now() - timedelta(days=3)).order_by(
            'upvote').reverse()[:8]
        article_list = Article.objects.filter(published=True, activated=True).reverse()
        return render(request, 'boards/board_index.html', {'user': user,
                                                           'article_list': article_list,
                                                           'article_list_top': article_list_top,
                                                           'error_message': '글을 쓰기 위해선 로그인 해주세요!'
                                                           })


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
                Attachment.objects.filter(article=A).update(activated=False)
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
                form = BasicForm(initial={'title':A.title,
                                          'article_text': A.article_text,
                                          })
                return render(request, 'boards/board_edit.html', {'article_edit': A,
                                                                  'form': form,
                                                                  })
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
                            activated=True,
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
    user = get_user(request)
    user_ip = get_client_ip(request)
    if CommentIpLog.objects.filter(ip=user_ip, comment=C).exists():
        return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': C.article_id}))
    else:
        if get_user(request).is_active:
            CommentIpLog.objects.create(ip=user_ip,
                                        user=user,
                                        comment=C,
                                        created_at=timezone.now())
        else:
            CommentIpLog.objects.create(ip=user_ip,
                                        comment=C,
                                        created_at=timezone.now())
        if request.method == 'POST':
            if request.POST['vote'] == 'up':
                C.upvote += 1
                C.save()
                return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': C.article_id}))
            if request.POST['vote'] == 'down':
                C.downvote += 1
                C.save()
                return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': C.article_id}))
            # up이랑 down 이랑 안되는 케이스도 어떻게 커버하는게 좋을듯
        elif request.method == 'GET':
            if request.GET['vote'] == 'up':
                C.upvote += 1
                C.save()
                return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': C.article_id}))
            if request.GET['vote'] == 'down':
                C.downvote += 1
                C.save()
                return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': C.article_id}))
        else:
            return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': C.article_id}))


def board_comment_delete(request, comment_id):
    C = get_object_or_404(Comment, pk=comment_id)
    user = get_user(request)
    if user.is_authenticated:
        if user == C.writer:
            C.activated = False
            C.save()
            return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': C.article_id,
                                                                               }))
        return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': C.article_id,
                                                                           }))
    return HttpResponseRedirect(reverse('boards:board_detail', kwargs={'article_id': C.article_id,
                                                                       }))


def board_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # request_user = get_user(request)
    article_list = Article.objects.filter(published=True, writer=user.id).reverse()
    PROFILE_IMG_URL = settings.BOARD_IMG_FTP

    template = 'boards/board_profile.html'
    page_fragment = 'boards/board_index_fragment.html'

    if request.is_ajax():
        template = page_fragment

    return render(request, template, {'user': user,
                                      'PROFILE_IMG_URL': PROFILE_IMG_URL,
                                      'page_fragment': page_fragment,
                                      'article_list': article_list,
                                      })

    # if user.is_authenticated :
    #     if user == request_user:
    #         return render(request, template, {'user': user,
    #                                           'page_fragment': page_fragment,
    #                                           'article_list': article_list,
    #                                           })
    #     else:
    #         return HttpResponseRedirect(reverse('boards:board_index'))
    # else:
    #     return HttpResponseRedirect(reverse('boards:board_index'))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# def board_navigator(request):
#     boards_activated_highest = Board.objects.filter(activated=True, has_higher_board=False).order_by('points').reverse()
#     boards_activated_has_higher = Board.objects.filter(activated=True, has_higher_board=True).order_by('points').reverse()
#     # boards_deactivated = Board.objects.filter(activated=False).order_by('created_at').reverse()
#     user = get_user(request)
#
#     return render(request, 'boards/board_navigator3.html', {'boards_activated_highest': boards_activated_highest,
#                                                            'boards_activated_has_higher': boards_activated_has_higher,
#                                                            'user': user,
#                                                             })


def board_navigator(request, **kwargs):
    user = get_user(request)
    boards_activated_highest = Board.objects.filter(activated=True, has_higher_board=False).order_by('points').reverse()

    template = 'boards/board_navigator.html'
    page_fragment = 'boards/board_project_list_fragment.html'

    if request.is_ajax():
        template = page_fragment

    if user.is_authenticated :
        return render(request, template, {'user': user,
                                          'page_fragment': page_fragment,
                                          'boards_activated_highest': boards_activated_highest})
    else:
        return render(request, template, {'boards_activated_highest': boards_activated_highest,
                                          'page_fragment': page_fragment,})


def board_navigator_under(request, board_id):
    user = get_user(request)
    board_self = get_object_or_404(Board, pk=board_id)
    boards_activated = Board.objects.filter(activated=True, higher_board=board_id).order_by('points').reverse()

    template = 'boards/board_navigator_under.html'
    page_fragment = 'boards/board_project_list_fragment.html'

    if request.is_ajax():
        template = page_fragment

    if user.is_authenticated :
        return render(request, template, {'user': user,
                                          'page_fragment': page_fragment,
                                          'boards_activated_highest': boards_activated,
                                          'board_self': board_self})
    else:
        return render(request, template, {'boards_activated_highest': boards_activated,
                                          'board_self': board_self,
                                          'page_fragment': page_fragment,})


def board_create_project_page(request):
    boards_activated_highest = Board.objects.filter(activated=True, has_higher_board=False).order_by('points').reverse()
    boards_activated_has_higher = Board.objects.filter(activated=True, has_higher_board=True).order_by('points').reverse()
    user = get_user(request)
    if user.is_authenticated:
        return render(request, 'boards/board_create_project.html', {'user': user,
                                                                    'boards_activated_highest': boards_activated_highest,
                                                                    })
    else:
        boards_activated_highest = Board.objects.filter(activated=True, has_higher_board=False).order_by(
            'points').reverse()

        template = 'boards/board_navigator.html'
        page_fragment = 'boards/board_project_list_fragment.html'

        if request.is_ajax():
            template = page_fragment

        else:
            return render(request, template, {'boards_activated_highest': boards_activated_highest,
                                              'error_message': '프로젝트를 개설하기 위해선 로그인 해주시길 바랍니다.',
                                              'page_fragment': page_fragment, })


def board_create_project(request, *args, **kwargs):
    if request.method == 'POST':
        boards_activated_highest = Board.objects.filter(activated=True, has_higher_board=False).order_by('points').reverse()

        user = get_user(request)
        if user.is_authenticated:
            has_higher = False
            if request.POST['higher_board'] == 'none':
                has_higher = False
            else:
                has_higher = True

            creator_public = True
            if request.POST['creator_public'] == 'true':
                creator_public = True
            else:
                creator_public = False

            if request.POST['higher_board'] == 'none':
                higher_board = None
            else:
                higher_board = get_object_or_404(Board, id=request.POST['higher_board'])

            newBoard = Board()

            newBoard.name = request.POST['name']
            newBoard.has_higher_board = has_higher
            newBoard.description = request.POST['description']
            newBoard.creator_public = creator_public
            newBoard.created_at = timezone.now()
            newBoard.creator = user
            newBoard.higher_board = higher_board

            kwargs = request.POST.copy()
            kwargs.pop("name", None)
            kwargs.pop("description", None)
            kwargs.pop("creator_public", None)
            kwargs.pop("higher_board", None)

            if len(request.FILES) != 0:
                file = request.FILES['board_image']
                kwargs.pop("csrfmiddlewaretoken", None)
                try:
                    board_image = BoardImage()
                    board_image.file = file
                    board_image.name = file.name

                    board_image.save(**kwargs)
                    newBoard.image_file = board_image
                except IOError:
                    newBoard.delete()
                    return render(request, 'boards/board_create_project.html', {'user': user,
                                                                                'error_message': '프로젝트 생성에 실패했습니다.',
                                                                                'boards_activated_highest': boards_activated_highest,
                                                                                })
            if higher_board:
                higher_board.has_lower_board = True
                higher_board.save()
            newBoard.save()
            return HttpResponseRedirect(reverse('boards:board_navigator'))
        else:
            return HttpResponseRedirect(reverse('boards:board_index'))
    else:
        return HttpResponseRedirect(reverse('boards:board_index'))