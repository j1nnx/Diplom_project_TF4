from django.urls import path

from config import settings
from diary.apps import DiaryConfig
from django.conf.urls.static import static
from diary.views import PostCreateView, PostListView, PostDetailView, PostUpdateView, PostDeleteView, SearchView

app_name = DiaryConfig.name

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('', PostListView.as_view(), name='list_posts'),
    path('detail/<int:pk>/', PostDetailView.as_view(), name='detail_post'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='update_post'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete_post'),
    path('search/', SearchView.as_view(), name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
