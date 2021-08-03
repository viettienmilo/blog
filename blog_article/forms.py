from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
	rating = forms.IntegerField(min_value=1, max_value=5, initial=5)

	class Meta:
		model = Comment
		fields = ('content', 'rating',)
