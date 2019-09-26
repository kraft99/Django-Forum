from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
	email = forms.CharField(max_length=255,
		help_text='Gmail account only.',
		widget=forms.EmailInput(attrs={'placeholder':'your email'}))
	class Meta:
		model = User
		fields = ['username','email','password1','password2']



	def clean_email(self):

		email = self.cleaned_data['email']
		required_domains = ['gmail']
		domain = email.split('@',1)[-1].split('.')[0].lower() 

		if not domain in required_domains:
			#user is not submitting the required domain.
			raise forms.ValidationError("Please,use Gmail account,\
				{0} is not a valid domain".format(domain))
		if User.objects.filter(email = email).exists():
			#user enters email that already exists in database.
			raise forms.ValidationError("Sorry,email already exists")
		return email
