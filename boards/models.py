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

    image = models.CharField(max_length=200, null=True)

    writer = models.ForeignKey(User, on_delete=models.CASCADE)

    comment_count = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    shared = models.IntegerField(default=0)

    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)

    published = models.BooleanField(default=False)
    activated = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']


class ArticleIpLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField('Date published')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    ip = models.GenericIPAddressField()


class Comment(models.Model):
    comment_text = models.TextField()
    created_at = models.DateTimeField('Date published')
    edited_at = models.DateTimeField('Latest edited date')

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writers')

    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)

    activated = models.BooleanField(default=False)

    class Meta:
        unique_together = ('id', 'article')
        ordering = ['id']

    def __str__(self):
        return '%d: %s: %d: %d: %s' % (self.id, self.writer, self.upvote, self.downvote, self.comment_text)


class CommentIpLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField('Date published')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    ip = models.GenericIPAddressField()


class Attachment(AbstractAttachment):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    activated = models.BooleanField(default=False)