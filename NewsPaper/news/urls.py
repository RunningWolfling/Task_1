from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, ArticleUpdate, ArticleDelete

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='news.urls'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/create/', PostCreate.as_view(), name='article_create'),
    path('<int:pk>/update/', ArticleUpdate.as_view, name='article_update'),
    path('<int:pk>/delete/', ArticleDelete.as_view, name='article_delete'),
]