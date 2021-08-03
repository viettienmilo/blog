from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email',)
	list_filter = ()
	search_fields = ("username__startswith",)
