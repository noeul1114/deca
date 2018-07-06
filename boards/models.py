import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    article_text = models.TextField()
    created_at = models.DateTimeField('Date published')