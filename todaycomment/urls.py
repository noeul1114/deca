from django.urls import path

from . import views

app_name = 'todaycomment'
urlpatterns = [
    path('', views.com_index, name='com_index'),
    path('post', views.com_post, name='com_post'),
    path('delete', views.com_delete, name='com_delete'),
]