from django.http.response import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import get_user

from django.utils import timezone

from django.shortcuts import get_object_or_404


from ..models import Article,  Comment, CommentIpLog



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


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip