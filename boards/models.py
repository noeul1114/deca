import datetime

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=200)
    article_text = models.TextField()
    created_at = models.DateTimeField('Date published')
    edited_at = models.DateTimeField('Latest edited date', auto_now=True)

    writer = models.ForeignKey(User, on_delete=models.CASCADE)

    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)


class Comment(models.Model):
    comment_text = models.TextField()
    created_at = models.DateTimeField('Date published')
    edited_at = models.DateTimeField('Latest edited date')

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)

    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)