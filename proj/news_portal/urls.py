from django.urls import path
from .views import *

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', PostSearch.as_view()),

    path('news/create/', NewsCreate.as_view()),
    path('news/<int:pk>/edit/', NewsEdit.as_view()),
    path('news/<int:pk>/delete/', NewsDelete.as_view()),

    path('article/create/', ArticleCreate.as_view()),
    path('article/<int:pk>/edit/', ArticleEdit.as_view()),
    path('article/<int:pk>/delete/', ArticleDelete.as_view()),
]
