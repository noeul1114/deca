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

from ..models import Article, ArticleIpLog, Comment, CommentIpLog, Board
from ..models import Attachment, Board, AdditionalUserProfile, BoardImage, UserProfileImage
from ..form import BasicForm, UserRegisterForm, UserRegisterFormOptional

from bs4 import BeautifulSoup



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


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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