from django.urls import path

from .views import (
    ArticleListView,
    ArticleDetailCommentView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
    CommentUpdateView,
    CommentDeleteView,
    UserArticleListView,
    CategoryArticleListView,
    TaggedArticleListView,
    ArticleSearchView,
)

app_name = 'blog_article'

urlpatterns = [
        path('', ArticleListView.as_view(), name='article_list'),
        path('article/<str:username>/', UserArticleListView.as_view(), name='user_article'),
        path('article/cat/<str:categoryname>/', CategoryArticleListView.as_view(), name='category_article'),
        path('article/tag/<str:tagslug>/', TaggedArticleListView.as_view(), name='tagged_article'),
        path('<int:year>/<int:month>/<int:day>/<slug:slug>/', ArticleDetailCommentView.as_view(), name='article_detail'),
        path('new/', ArticleCreateView.as_view(), name='article_create'),
        path('<int:year>/<int:month>/<int:day>/<slug:slug>/update/', ArticleUpdateView.as_view(), name='article_update'),
        path('<int:year>/<int:month>/<int:day>/<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
        path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
        path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
        path('article/<str:username>/', UserArticleListView.as_view(), name='user_article'),
        path('article/cat/<str:categoryname>/', CategoryArticleListView.as_view(), name='category_article'),
        path('article/', ArticleSearchView.as_view(), name='article_search'),
    ]
