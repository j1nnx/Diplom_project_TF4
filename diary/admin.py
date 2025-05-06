from django.contrib import admin
from diary.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """ Панель статей в админке """
    list_display = ('id', 'title', 'author', 'created_at')