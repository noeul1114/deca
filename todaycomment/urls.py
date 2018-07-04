from django.urls import path

from . import views

app_name = 'todaycomment'
urlpatterns = [
    path('', views.index, name='index'),
    path('post', views.post, name='post'),
    path('delete', views.delete, name='delete'),
]