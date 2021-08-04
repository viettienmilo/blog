from ._base import *

DEBUG = False
ADMINS = (
		('Nguyen Viet Tien', 'pymail.milo@gmail.com')
)

ALLOWED_HOSTS = ['*']
SECRET_KEY = 'cd97f9bc9d0599bd866f77f44877e4c0e41e5e574171d6e30dfa1d3be3392fa27c76fc1ba13b3ed682c0bd9ba77dcc8731558b7ed65963a11f67a1f3260e0c2f'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'blog_db',
		'USER': '',
		'PASSWORD': '',
		'OPTIONS': {'charset': 'utf8mb4'},
	}
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
