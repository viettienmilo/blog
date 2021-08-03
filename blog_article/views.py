from taggit.models import Tag
from ckeditor.fields import RichTextField

from django.db.models import Count, Q, CharField
from django.db.models.functions import Lower
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
	FormView,
)
from django.views import View
from django.views.generic.detail import SingleObjectMixin

from .models import Article, Comment, Category
from .forms import CommentForm
from users.models import User

CharField.register_lookup(Lower, "lower")
RichTextField.register_lookup(Lower, "lower")


class ArticleListView(ListView):
	model = Article
	context_object_name = 'articles'
	paginate_by = 3
	# paginate_orphans = 1

	def get_queryset(self):
		articles = Article.publishes.all()
		return articles


class TaggedArticleListView(ListView):
	model = Article
	context_object_name = 'articles'
	paginate_by = 3
	# paginate_orphans = 1

	def get_queryset(self):
		tag = get_object_or_404(Tag, slug=self.kwargs.get('tagslug'))
		articles = Article.publishes.filter(tags__in=[tag])
		return articles


class UserArticleListView(ListView):
	model = Article
	context_object_name = 'articles'
	template_name = 'blog_article/user_article_list.html'
	paginate_by = 3
	# paginate_orphans = 1

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		articles = Article.publishes.filter(author=user).order_by('-date_published')
		return articles


class CategoryArticleListView(ListView):
	model = Article
	context_object_name = 'articles'
	template_name = 'blog_article/category_article_list.html'
	paginate_by = 3
	# paginate_orphans = 1

	def get_queryset(self):
		category = get_object_or_404(Category, name=self.kwargs.get('categoryname'))
		articles = Article.publishes.filter(category=category).order_by('-date_published')
		return articles


class ArticleDetailView(DetailView):
	model = Article
	context_object_name = 'article'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = CommentForm()

		article = self.get_object()
		article_tag_ids = article.tags.values_list('id', flat=True)
		similar_articles = Article.publishes.filter(tags__in=article_tag_ids).exclude(id=article.id)
		similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-date_published')[:5]
		context['similar_articles'] = similar_articles

		return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
	model = Article
	fields = ('title', 'category', 'tags', 'content', 'coverimage', 'status', )
	context_object_name = 'article'

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.slug = slugify(form.instance.title)
		return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Article
	fields = ('title', 'category', 'tags', 'content', 'coverimage', 'status')
	context_object_name = 'article'

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.slug = slugify(form.instance.title)
		return super().form_valid(form)

	def test_func(self):
		article = self.get_object()
		if self.request.user == article.author:
			return True
		return False


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Article
	context_object_name = 'article'
	success_url = reverse_lazy('blog_article:article_list')

	def test_func(self):
		article = self.get_object()
		if self.request.user == article.author:
			return True
		return False


class CommentView(SingleObjectMixin, FormView):
	form_class = CommentForm
	fields = ('content', 'rating', )
	template_name = 'blog_article/article_detail.html'
	model = Article

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return HttpResponseForbidden()
		self.object = self.get_object()
		return super().post(request, *args, **kwargs)

	def form_valid(self, form):
		# article = get_object_or_404(Article, id=self.kwargs.get('article_id'))
		comment = form.save(commit=False)
		comment.article = self.object
		comment.user = self.request.user
		comment.save()
		return super(CommentView, self).form_valid(form)

	def get_success_url(self):
		# article = get_object_or_404(Article, id=self.kwargs.get('article_id'))
		article = self.object
		return reverse_lazy(
				'blog_article:article_detail',
				args=[article.date_published.year,
						article.date_published.month,
						article.date_published.day,
						article.slug])


class ArticleDetailCommentView(View):
	def get(self, request, *args, **kwargs):
		view = ArticleDetailView.as_view()
		return view(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		view = CommentView.as_view()
		return view(request, *args, **kwargs)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
	model = Comment
	form_class = CommentForm
	context_object_name = 'comment'
	success_message = 'Your comment has been updated successfully!'

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)

	def test_func(self):
		comment = self.get_object()
		if self.request.user == comment.user:
			return True
		return False

	def get_success_url(self):
		comment = self.get_object()
		article = comment.article
		return reverse_lazy(
				'blog_article:article_detail',
				args=[article.date_published.year,
						article.date_published.month,
						article.date_published.day,
						article.slug])


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Comment
	context_object_name = 'comment'

	def test_func(self):
		comment = self.get_object()
		if self.request.user == comment.user:
			return True
		return False

	def get_success_url(self):
		comment = self.get_object()
		article = comment.article
		return reverse_lazy(
				'blog_article:article_detail',
				args=[article.date_published.year,
						article.date_published.month,
						article.date_published.day,
						article.slug])


class ArticleSearchView(ListView):
	model = Article
	context_object_name = 'articles'
	tamplate_name = 'blog_article/search_results.html'
	paginate_by = 3
	# paginate_orphans = 1

	def get_queryset(self):
		query = self.request.GET.get('search').lower()
		if query:
			# query_articles = Article.publishes.filter(Q(title__lower__contains=query) | Q(content__lower__contains=query) | \
			# 											Q(slug__lower__contains=query))
			query_articles = Article.publishes.filter(
				Q(title__lower__contains=query) | Q(content__lower__contains=query))
		return query_articles
