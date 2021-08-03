from django import forms


class ArticleShareForm(forms.Form):
	recipient = forms.EmailField(max_length=150, required=True, help_text='Enter Recipient Email.')
	suggestion = forms.CharField(required=False, widget=forms.Textarea)
