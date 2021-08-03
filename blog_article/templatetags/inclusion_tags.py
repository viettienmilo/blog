from django import template

from main.core.utils import rating_average
from blog_article.models import Article, Category

register = template.Library()


@register.inclusion_tag('blog_article/latest_articles.html')
def latest_articles(max_num=5):
	latest = Article.publishes.order_by('-date_published')[:max_num]
	return {'latest_articles': latest}


@register.inclusion_tag('blog_article/top_rating_articles.html')
def top_rating_articles(max_num=5):
	articles = Article.publishes.all()
	article_dict = {}
	for article in articles:
		rating = rating_average([comment.rating for comment in article.comment_set.all()])
		article_dict.update({article: rating})

	sort_article_dict = sorted(article_dict.items(), key=lambda x: x[1], reverse=True)
	top_articles = sort_article_dict[:max_num]
	return {'top_rating_articles': top_articles}


@register.inclusion_tag('blog_article/category_list.html')
def get_categories():
	categories = Category.objects.all()
	return {'categories': categories}
