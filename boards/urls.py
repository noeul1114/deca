from django.urls import path

from . import views

app_name = 'boards'
urlpatterns = [
    path('', views.board_index, name='board_index'),
    path('login/', views.board_login, name='board_login'),
    path('logout/', views.board_logout, name='board_logout'),
    path('register/', views.board_register, name='board_register'),

    # path('write/', views.board_write, name='board_write'),
    path('delete/<int:article_id>', views.board_delete, name='board_delete'),
    path('delete_fix/', views.board_delete_fix, name='board_delete_fix'),

    path('edit/<int:article_id>', views.board_edit, name='board_edit'),
    path('edit_fix/', views.board_edit_fix, name='board_edit_fix'),
    path('<int:article_id>/', views.board_detail, name='board_detail'),
    path('vote/<int:article_id>', views.board_vote, name='board_vote'),

    path('comment/', views.board_comment_write, name='board_comment_write'),
    path('comment_vote/<int:comment_id>', views.board_comment_vote, name='board_comment_vote'),
    path('comment_delete/<int:comment_id>', views.board_comment_delete, name='board_comment_delete'),
    path('profile/<int:user_id>', views.board_profile, name='board_profile'),

    path('navigatior/', views.board_navigator, name='board_navigator'),
    path('projectCreatePage/', views.board_create_project_page, name='board_create_project_page'),
    path('projectCreate/', views.board_create_project, name='board_create_project'),

    path('write/', views.board_write, name='board_write'),
]