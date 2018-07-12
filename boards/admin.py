from django.contrib import admin

from .models import Comment, Article

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


admin.site.register(Article, ArticleAdmin)