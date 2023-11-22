import django_filters
from django_filters import FilterSet
from .models import Post, Author
from django import forms

class PostFilter(FilterSet):
    head = django_filters.CharFilter(field_name='head', label='Поиск', lookup_expr='icontains', )
    author = django_filters.ModelChoiceFilter(field_name='author', label='Выбрать автора', lookup_expr='exact', queryset=Author.objects.all())
    time_in = django_filters.DateFilter(field_name='time_create', widget=forms.DateInput(attrs={'type': 'date'}), label='Дата', lookup_expr='date__gte')
    class Meta:
        model = Post
        fields = {
            'head',
            'author',
            'time_in',
        }
