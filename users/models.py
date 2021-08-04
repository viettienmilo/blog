from PIL import Image

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	email = models.EmailField(verbose_name='email', max_length=60, unique=True)
	avatar = models.ImageField(upload_to='avatar/%Y/%m', default='default.png')

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', ]

	def __str__(self):
		return self.username

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.avatar.path)
		if img.width > 150 or img.height > 150:
			output_size = (150, 150)
			img.thumbnail(output_size)
		img.save(self.avatar.path)
