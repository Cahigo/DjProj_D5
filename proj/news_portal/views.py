from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from .filters import PostsFilter


class PostsList(ListView):
    model = Post  # Модель для View
    ordering = 'created'  # Поле, по которому будет идти сортировка
    template_name = 'posts.html'  # Название HTML-шаблона
    context_object_name = 'posts'  # Имя списка, в котором будут лежать все объекты
    paginate_by = 2  # Пагинация
    filterset = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
