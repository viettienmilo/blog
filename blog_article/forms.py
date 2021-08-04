from django import forms

from .models import Comment

RATING_CHOICES = (
		('0', '☆☆☆☆☆'),
		('1', '★☆☆☆☆'),
		('2', '★★☆☆☆'),
		('3', '★★★☆☆'),
		('4', '★★★★☆'),
		('5', '★★★★★'),
)


class CommentForm(forms.ModelForm):
	rating = forms.ChoiceField(choices=RATING_CHOICES, initial=RATING_CHOICES[3])

	class Meta:
		model = Comment
		fields = ('content', 'rating',)
