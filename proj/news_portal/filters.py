import django_filters
from django import forms
from django_filters import FilterSet, DateTimeFilter
from django.db import models

from .models import Post


class PostsFilter(FilterSet):
    created = DateTimeFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='date__gt'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'username': ['exact'],
        }
