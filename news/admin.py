from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import News, NewsCategory, TagNews


@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'image', 'post_image', 'updated_at', 'is_published', 'category')
    prepopulated_fields = {'slug': ('name', )}
    readonly_fields = ['post_image']
    list_display_links = ('id', 'name')
    ordering = ['-created_at']
    list_editable = ('is_published', 'category')
    list_filter = ['category__name', 'is_published']

    @admin.display(description='Изображение', ordering='content')
    def post_image(self, news: News):
        if news.image:
            return mark_safe(f"<img src='{news.image.url}' width=50>")
        return 'Нет фото'


@admin.register(NewsCategory)
class AdminNewsCategory(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(TagNews)
class AdminTagNews(admin.ModelAdmin):
    list_display = ('id', 'tag')
    list_display_links = ('id', 'tag')
