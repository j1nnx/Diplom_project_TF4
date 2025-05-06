from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, View
from django.db.models import Q
from diary.forms import PostForm
from diary.models import Post
from django.core.paginator import Paginator


class PostCreateView(LoginRequiredMixin, CreateView):
    """ Создание статьи в дневнике """
    model = Post
    form_class = PostForm
    template_name = 'diary/post_create.html'
    success_url = reverse_lazy('diary:list_posts')

    def form_valid(self, form):
        """ Сохраняет объект модели, установив автора записи """
        if form.is_valid():
            post = form.save(commit=False)
            post.author = self.request.user  # Присваиваем текущему пользователю
            post.save()
            return super().form_valid(form)
        else:
            print(form.errors)  # Выведет ошибки формы в консоль
            return self.form_invalid(form)  # Возвращаем ошибки формы


class PostListView(LoginRequiredMixin, ListView):
    """ Просмотр всех статей """
    model = Post
    template_name = 'diary/index.html'
    context_object_name = 'posts'
    paginate_by = 5  # Укажите количество записей на странице

    def get_queryset(self):
        # Возвращаем только те посты, которые принадлежат текущему пользователю
        return Post.objects.filter(author=self.request.user)


class PostDetailView(LoginRequiredMixin, DetailView):
    """ Просмотр статьи """
    model = Post
    template_name = 'diary/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        # Возвращаем только те посты, которые принадлежат текущему пользователю
        return Post.objects.filter(author=self.request.user)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """ Изменение статьи """
    model = Post
    form_class = PostForm
    template_name = 'diary/post_update.html'
    success_url = reverse_lazy('diary:list_posts')

    def get_queryset(self):
        # Возвращаем только те посты, которые принадлежат текущему пользователю
        return Post.objects.filter(author=self.request.user)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаление статьи """
    model = Post
    template_name = 'diary/post_delete.html'
    success_url = reverse_lazy('diary:list_posts')

    def get_queryset(self):
        # Возвращаем только те посты, которые принадлежат текущему пользователю
        return Post.objects.filter(author=self.request.user)


class SearchView(View):
    """ Контроллер для поиска статьи """

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        results = ''
        if query:
            results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        paginator = Paginator(results, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'diary/search.html',
                      context={'title': 'Поиск', 'results': page_obj, 'count': paginator.count})

    def get_queryset(self):
        # Возвращаем только те посты, которые принадлежат текущему пользователю
        return Post.objects.filter(author=self.request.user)
