from boards.models import Article, Comment
from django.contrib.auth.models import User
from django.urls import path, include, re_path

from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','comment_text', 'upvote', 'downvote', 'writer_id', 'article_id', 'activated', 'created_at')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'image', 'upvote', 'comment_count', 'downvote', 'published')


class ArticleDetailSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Article
        fields = ('id', 'article_text', 'title', 'board', 'comments',
                  'image', 'upvote', 'comment_count','likes','shared', 'hit',
                  'downvote', 'published', 'activated', 'created_at', 'edited_at',
                  'writer_id')


# ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(published=True, activated=True).order_by('upvote').reverse()
    serializer_class = ArticleSerializer


class ArticleDetailViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(published=True, activated=True)
    serializer_class = ArticleDetailSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'articleDetail', ArticleDetailViewSet)
router.register(r'comment', CommentViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls')),
]
