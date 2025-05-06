from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ Панель пользователи  в админке """
    list_display = ('email', 'id', 'phone',)
