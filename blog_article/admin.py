from django.contrib import admin

from .models import Category, Article, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'description',)
	list_filter = ('name',)
	search_fields = ('name__startswith',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'date_created', 'date_published')
	list_filter = ('status', 'date_created', 'date_published', 'author')
	search_fields = ('name__startswith', 'content__contains')
	prepopulated_fields = {'slug': ('title',)}
	date_hierarchy = 'date_published'
	ordering = ('-date_published', 'status')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('article', 'user', 'rating', 'content', 'date_created', 'active')
	list_filter = ('active', 'date_created', 'date_updated', 'user')
	search_fields = ('user', 'content')
