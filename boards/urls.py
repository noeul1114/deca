from django.urls import path

from . import views

app_name = 'boards'
urlpatterns = [

    path('', views.board_index, name='board_index'),
    path('login/', views.board_login, name='board_login'),
    path('logout/', views.board_logout, name='board_logout'),
    path('register/', views.board_register, name='board_register'),

    path('write/', views.board_write, name='board_write'),
    path('delete/', views.board_delete, name='board_delete'),
    path('edit/', views.board_edit, name='board_edit'),
    path('edit_fix/', views.board_edit_fix, name='board_edit_fix'),

    path('<int:article_id>/', views.board_detail, name='board_detail'),

    path('vote/<int:article_id>', views.board_vote, name='board_vote'),
    path('comment/', views.board_comment_write, name='board_comment_write'),
    path('comment_vote/<int:comment_id>', views.board_comment_vote, name='board_comment_vote'),
]