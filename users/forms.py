from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegForm(UserCreationForm):
	email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

	class Meta:
		model = User
		fields = ('email', 'username', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'avatar']
