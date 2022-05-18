from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import Writer


class NewWriterForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = Writer
		fields = ("username", "first_name", "last_name", "is_editor", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewWriterForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user