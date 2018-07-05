from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from django.urls import reverse

from django.http import HttpResponseRedirect
from .models import Comment_list

# Create your views here.

def com_index(request):
    comment_list = Comment_list.objects.order_by('created_at').reverse()
    return render(request, 'todaycomment/index.html', {'comment_list': comment_list})

def com_post(request):
    try:
        C = Comment_list(comment_text=request.POST['comment_text'], created_at=timezone.now())
        C.save()
        return HttpResponseRedirect(reverse('todaycomment:com_index'))
    except:
        return render(request, 'todaycomment/index.html', {'error_message': "댓글을 쓰는데에 실패했습니다."})

def com_delete(request):
    C = get_object_or_404(Comment_list, id=request.POST['comment_del'])
    try:
        C.delete()
        return HttpResponseRedirect(reverse('todaycomment:com_index'))
    except:
        return render(request, 'todaycomment/index.html', {'error_message' : "댓글을 삭제하는데에 실패했습니다."})