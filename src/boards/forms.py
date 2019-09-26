from django import forms
from .import models



class NewTopicForm(forms.ModelForm):
	message = forms.CharField(
		widget=forms.Textarea(attrs={'rows':5,'placeholder':'What is on your mind bro ?'}),
		max_length=250,
		help_text="The max length of text is 250")

	class Meta:
		model  = models.Topic
		fields = ['subject','message']
	 



class PostForm(forms.ModelForm):

	class Meta:
		model = models.Post
		fields = ['message',]



# class EditPostForm(forms.ModelForm):

# 	class Meta:
# 		model = models.Post
# 		fields = ['message',]


