from django.contrib import admin

from .models import Article, Comment, Category

admin.site.register(Category)
# admin.site.register(Article)
admin.site.register(Comment)

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('category', 'author_nickname', 'article_title', 'article_text', 'pub_date')
        }),
        )
    # fields = ['author_nickname', 'article_title', 'article_text', 'pub_date']
    # list_display = ('article_title', 'author_nickname','pub_date')

admin.site.register(Article, ArticleAdmin)