import datetime

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from django_summernote.models import AbstractAttachment

# Create your models here.


class Vote(models.Model):
    created_at = models.DateTimeField('Date published')
    voter = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ip = models.GenericIPAddressField()

    up_down = models.BooleanField(default=True)


class Article(models.Model):
    title = models.CharField(max_length=200)
    article_text = models.TextField()
    created_at = models.DateTimeField('Date published')
    edited_at = models.DateTimeField('Latest edited date', auto_now=True)

    writer = models.ForeignKey(User, on_delete=models.CASCADE)

    comment_count = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    shared = models.IntegerField(default=0)

    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)

    published = models.BooleanField(default=False)
    activated = models.BooleanField(default=False)


class Comment(models.Model):
    comment_text = models.TextField()
    created_at = models.DateTimeField('Date published')
    edited_at = models.DateTimeField('Latest edited date')

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)

    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)

    activated = models.BooleanField(default=False)


class Attachment(AbstractAttachment):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    activated = models.BooleanField(default=False)