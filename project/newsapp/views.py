from django.views.generic import ListView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'news_page.html'
    context_object_name = 'posts'
