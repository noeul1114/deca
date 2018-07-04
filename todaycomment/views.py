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
    C = Comment_list(comment_text=request.POST['comment_text'], created_at=timezone.now())
    try:
        C.save()
        return HttpResponseRedirect(reverse('todaycomment:com_index'))
    except:
        return HttpResponseRedirect('todaycomment:com_index')

def com_delete(request):
    C = Comment_list.objects.get(id=request.POST['comment_del'])
    try:
        C.delete()
        return HttpResponseRedirect(reverse('todaycomment:com_index'))
    except:
        return HttpResponseRedirect('todaycomment:com_index')