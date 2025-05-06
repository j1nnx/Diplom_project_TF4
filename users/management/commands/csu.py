from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """ Кастомная команда для создания суперпользователя """
    def handle(self, *args, **options):
        user = User.objects.create(email="admin@admin.ru")
        user.set_password("123")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Успешно создан суперпользователь с email {user.email}"))
