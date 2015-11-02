from django.contrib import admin

from .models import Article, Comment, Category

admin.site.register(Category)
admin.site.register(Comment)

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('category', 'article_title', 'article_text', 'pub_date')
        }),
        )

admin.site.register(Article, ArticleAdmin)