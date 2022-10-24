from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from .tasks import notify_about_new_post


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'flatpages/news_page.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/one_news_page.html'
    context_object_name = 'posts_one'


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('newsapp.add_post')
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'

    def add_notify_about_new_post(self, request):
        notify_about_new_post.delay()
        return render(request)


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsapp.change_post')
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newsapp.delete_post')
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryListView(ListView):
    model = Post
    template_name = 'flatpages/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['postCategory'] = self.postCategory
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'You have successfully subscribed to the newsletter of the category:'
    return render(request, 'flatpages/subscribe.html', {'category': category, 'message': message})
