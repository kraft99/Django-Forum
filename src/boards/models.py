import math
import uuid
# markdown utilities
from django.utils.html import mark_safe
from markdown import markdown

from django.conf import settings
from django.utils.text import Truncator
from django.db import models




class Board(models.Model):
	"""
	Board Model
	"""
	id   		= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name 		= models.CharField(max_length=125,unique=True)
	description = models.TextField(max_length = 255)

	created		= models.DateTimeField(auto_now_add = True)
	updated		= models.DateTimeField(auto_now = True)


	class Meta:
		ordering = ['-created']
		verbose_name = 'Board'
		verbose_name_plural = 'Boards'


	def __str__(self):

		return self.name if self.name else None


	@property	
	def get_posts_count(self):

		return Post.objects.filter(topic__board = self).count()

	@property
	def get_last_post(self):

		return Post.objects.filter(topic__board = self).first()
	






class Topic(models.Model):
	"""
	Topic Model
	"""
	id   		= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	subject     = models.CharField(max_length=125)
	board       = models.ForeignKey(Board,related_name='topics',on_delete=models.SET_NULL,null=True)
	starter 	= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_topics')
	views 		= models.PositiveSmallIntegerField(default = 0) #viewers counter

	created		= models.DateTimeField(auto_now_add = True)
	updated		= models.DateTimeField(auto_now = True)


	class Meta:
		ordering = ['-created']
		verbose_name = 'Topic'
		verbose_name_plural = 'Topics'


	def __str__(self):
		return "{0} by {1}".format(self.subject,
			self.starter.username) if self.starter and self.subject else None


	def get_page_count(self):
		count = self.posts.count()
		pages = count/2 #pagination number
		return math.ceil(pages)


	def get_last_3_posts(self):

		return self.posts.all()[:3]



	def has_many_pages(self,count=None):
		if count is None:
			count = self.get_page_count()
		return count > 2


	def get_page_range(self):
		count = self.get_page_count()
		if self.has_many_pages(count):
			return range(1,3)
		return range(1,count + 1)




class Post(models.Model):
	"""
	Post Model
	"""
	id   		= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	message		= models.TextField(max_length=125)
	topic 		= models.ForeignKey(Topic,related_name='posts',on_delete=models.CASCADE)
	created_by  = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user_posts',on_delete=models.CASCADE)
	updated_by  = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='+',null=True,on_delete=models.SET_NULL)

	created		= models.DateTimeField(auto_now_add = True)
	updated		= models.DateTimeField(auto_now = True)


	class Meta:
		ordering = ['-created']
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'


	def __str__(self):
		message_truc_obj = Truncator(self.message)
		return message_truc_obj.chars(13)


	def get_message_as_markdown(self):
		return mark_safe(markdown(self.message,safe_mode='escape'))

