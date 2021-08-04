from PIL import Image
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

from django.db import models
from django.utils import timezone
from django.urls import reverse

from users.models import User

################################################################################################################
#                MANAGERS                                                                                      #
################################################################################################################


class PublishManager(models.Manager):
	def get_queryset(self):
		return super(PublishManager, self).get_queryset().filter(status='publish')


class DraftManager(models.Manager):
	def get_queryset(self):
		return super(DraftManager, self).get_queryset().filter(status='draft')


################################################################################################################
#                MODELS                                                                                        #
################################################################################################################


class Category(models.Model):
	name = models.CharField(max_length=190, verbose_name='Category')
	description = models.TextField(verbose_name='Description')

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name


class Article(models.Model):
	STATUS_CHOICES = (
			('draft', 'Draft'),
			('publish', 'Publish'),
	)

	title = models.CharField(max_length=190, verbose_name='Article Title')
	slug = models.SlugField(max_length=190, unique_for_date='date_published')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
	date_created = models.DateTimeField(auto_now_add=True, verbose_name='Create on')
	date_published = models.DateTimeField(default=timezone.now, verbose_name='Published on')
	date_updated = models.DateTimeField(auto_now=True, verbose_name='Updated on')
	content = RichTextField()
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Article Author')
	status = models.CharField(max_length=15, choices=STATUS_CHOICES, verbose_name='Article Status')
	coverimage = models.ImageField(upload_to='cover/%Y/%m/%d', default='coverimage.png')

	objects = models.Manager()
	publishes = PublishManager()
	drafts = DraftManager()
	tags = TaggableManager()

	class Meta:
		ordering = ('-date_published', 'title',)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.coverimage.path)
		if img.width > 600 or img.height > 600:
			output_size = (600, 600)
			img.thumbnail(output_size)
		img.save(self.coverimage.path)

	def get_absolute_url(self):
		return reverse('blog_article:article_detail', args=[self.date_published.year,
															self.date_published.month,
															self.date_published.day,
															self.slug])


class Comment(models.Model):
	article = models.ForeignKey(Article, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = RichTextField()
	rating = models.PositiveIntegerField(help_text='Rating from 0 to 5')
	date_created = models.DateTimeField(auto_now_add=True, verbose_name='Created on')
	date_updated = models.DateTimeField(auto_now=True, verbose_name='Updated on')
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('-date_created', )

	def __str__(self):
		return f'Comment from {self.user.username} on {self.article}'
