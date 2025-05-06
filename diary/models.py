from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Post(models.Model):
    """ Модель поста в дневнике """
    title = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(**NULLABLE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор статьи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикация статьи')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
