from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages

from .forms import RegForm, UserUpdateForm
from blog_article.models import Article


def register(request):
	if request.method == 'POST':
		form = RegForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(email=email, password=raw_password)
			login(request, user)
			messages.success(request, f'Welcome {username}. You have been registered succesfully and automatically logged in.')
			return redirect('blog_article:article_list')
	else:
		form = RegForm()
	context = {'form': form}
	return render(request, 'register.html', context)


@login_required
def profile(request):
	user = request.user
	group_permissions = user.get_group_permissions()
	user_permissions = user.get_user_permissions()

	published_articles = Article.publishes.filter(author__username=user.username).order_by('-date_published').all()
	draft_articles = Article.drafts.filter(author__username=user.username).order_by('-date_created').all()

	if request.method == 'POST':
		form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your profile has been updated successfully')
			return redirect('users:profile')
	else:
		form = UserUpdateForm(instance=request.user)

	context = {
			'group_permissions': group_permissions,
			'user_permissions': user_permissions,
			'published_articles': published_articles,
			'draft_articles': draft_articles,
			'form': form,
		}
	return render(request, 'profile.html', context)

