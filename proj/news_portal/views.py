from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import Post
from .filters import PostsFilter
from .forms import PostForm


class PostsList(ListView):
    model = Post  # Модель для View
    ordering = 'created'  # Поле, по которому будет идти сортировка
    template_name = 'posts.html'  # Название HTML-шаблона
    context_object_name = 'posts'  # Имя списка, в котором будут лежать все объекты
    paginate_by = 2  # Пагинация

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = 'created'
    template_name = 'search.html'
    context_object_name = 'search'
    filterset = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    success_url = '/'
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NWS'
        return super().form_valid(form)


class NewsEdit(UpdateView):
    form_class = PostForm
    model = Post
    success_url = '/'
    template_name = 'news_edit.html'


class NewsDelete(DeleteView):
    model = Post
    success_url = '/'
    template_name = 'news_delete.html'


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    success_url = '/'
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'ART'
        return super().form_valid(form)


class ArticleEdit(UpdateView):
    form_class = PostForm
    model = Post
    success_url = '/'
    template_name = 'article_edit.html'


class ArticleDelete(DeleteView):
    model = Post
    success_url = '/'
    template_name = 'article_delete.html'
