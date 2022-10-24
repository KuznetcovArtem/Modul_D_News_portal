from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page

from .views import PostList, PostDetail, PostCreate, PostEdit, PostDelete, CategoryListView, subscribe

urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('accounts/', include('allauth.urls')),
   path('<int:pk>/', cache_page(60*5), PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]
