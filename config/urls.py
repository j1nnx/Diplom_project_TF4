from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView

from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('users/', include('users.urls', namespace='users')),
    path('diary/', include('diary.urls', namespace='diary')),
    path("ckeditor/", include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)