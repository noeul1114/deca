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


class BoardAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['description']}),
        ('Date information', {'fields': ['created_at'], 'classes': ['collapse']}),
    ]
    list_display = ('name', 'description', 'points', 'image', 'creator', 'has_higher_board')
    list_filter = ['created_at']
    search_fields = ['name']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Board, BoardAdmin)