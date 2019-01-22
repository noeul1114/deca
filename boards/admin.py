from django.contrib import admin

from .models import Comment, Article, Board, BoardImage, Attachment, AdditionalUserProfile,\
    CommentIpLog, ArticleIpLog

# Register your models here.


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['article_text']}),
        ('Date information', {'fields': ['created_at'], 'classes': ['collapse']}),
    ]
    inlines = [CommentInline]
    list_display = ('title', 'article_text', 'writer')
    list_filter = ['created_at']
    search_fields = ['writer']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'upvote', 'writer')
    list_filter = ['created_at']


class BoardAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['description']}),
        ('Date information', {'fields': ['created_at'], 'classes': ['collapse']}),
    ]
    list_display = ('name', 'description', 'points', 'image', 'creator', 'has_higher_board')
    list_filter = ['created_at']
    search_fields = ['name']


class BoardIPLOG(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'ip', 'article_id', 'user_id')
    list_filter = ['created_at']


class BoardCommentIPLOG(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'ip', 'comment_id', 'user_id')
    list_filter = ['created_at']


admin.site.register(ArticleIpLog, BoardIPLOG)
admin.site.register(CommentIpLog, BoardCommentIPLOG)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Board, BoardAdmin)