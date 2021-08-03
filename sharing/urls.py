from django.urls import path

from .views import ArticleShareView

app_name = 'sharing'

urlpatterns = [
        path('<int:article_id>/share/', ArticleShareView.as_view(), name='article_share'),

    ]
