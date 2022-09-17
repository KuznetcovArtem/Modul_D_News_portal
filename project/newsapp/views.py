from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'flatpages/news_page.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/one_news_page.html'
    context_object_name = 'posts_one'

