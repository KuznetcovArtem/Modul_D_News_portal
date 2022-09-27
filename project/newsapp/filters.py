from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from django.forms import DateInput
from .models import Post, Author, Category


class PostFilter(FilterSet):
    postCategory = ModelChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='Select a category',
    )

    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Author',
        empty_label='Select a author',
    )

    # поиск позже указываемой даты
    creation_after = DateFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'},
        ),
    )

    class Meta:
        model = Post
        fields = {
           'title': ['icontains'], # поиск по названию
           }
