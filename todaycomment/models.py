from django.db import models

# Create your models here.


class Comment_list(models.Model):
    name = models.CharField(max_length=20)
    comment_text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_created='True')
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)

    def __str__(self):
        return self.comment_text

