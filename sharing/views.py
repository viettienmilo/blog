from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from blog_article.models import Article
from main.settings.dev import get_secret
from .forms import ArticleShareForm


class ArticleShareView(LoginRequiredMixin, FormView):
	form_class = ArticleShareForm
	template_name = "sharing/article_share.html"

	def form_valid(self, form):
		article = get_object_or_404(Article, id=self.kwargs.get('article_id'))
		article_url = self.request.build_absolute_uri(article.get_absolute_url())
		user = self.request.user
		host_email = get_secret('EMAIL_USERNAME')
		subject = f'{user.username} ({user.email}) recommendation'
		message = f'You should read {article.title} at following link {article_url}\n\n ' \
		          f'{user.username} suggestions: {form.cleaned_data["suggestion"]}'
		send_mail(subject, message, host_email, (form.cleaned_data["recipient"],))
		messages.success(self.request, f'A suggestion email has been sent to {form.cleaned_data["recipient"]}')
		return super().form_valid(form)

	def get_success_url(self):
		article = get_object_or_404(Article, id=self.kwargs.get('article_id'))
		return reverse_lazy(
				'blog_article:article_detail',
				args=[
						article.date_published.year,
						article.date_published.month,
						article.date_published.day,
						article.slug])
