from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from django.urls import reverse

from django.http import HttpResponseRedirect
from .models import Comment_list

# Create your views here.

def index(request):
    comment_list = Comment_list.objects.order_by('created_at').reverse()
    return render(request, 'todaycomment/index.html', {'comment_list': comment_list})

def post(request):
    C = Comment_list(comment_text=request.POST['comment_text'], created_at=timezone.now())
    try:
        C.save()
        return HttpResponseRedirect(reverse('todaycomment:index'))
    except:
        return HttpResponseRedirect('todaycomment:index')

def delete(request, id):
    C = Comment_list.objects.get(id=id)
    try:
        C.delete()
        return HttpResponseRedirect(reverse('todaycomment:index'))
    except:
        return HttpResponseRedirect('todaycomment:index')