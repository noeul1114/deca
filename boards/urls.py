from django.urls import path

from . import views

app_name = 'boards'
urlpatterns = [
    path('', views.board_index, name='board_index'),
    path('login/', views.board_login, name='board_login'),
    path('register/', views.board_register, name='board_register'),
]