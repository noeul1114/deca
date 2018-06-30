from django.shortcuts import render

from . import models

# Create your views here.

def index(request):
    comment_list = models.Comment_list.objects.order_by('created_at')
    return render(request, 'todaycomment/index.html', {'comment_list': comment_list})