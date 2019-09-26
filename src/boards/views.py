from django.utils import timezone
from django.db.models import Count
from django.urls import resolve,reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect

# Generic Views
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView,ListView

from .forms import NewTopicForm,PostForm
from .models import Board,Topic,Post


# def board_index(request):

# 	context  = dict()
# 	boards = Board.objects.all()
# 	template = 'boards/index.html'

# 	context['boards'] = boards
# 	return render(request,template,context)


class BoardListView(ListView):

	model = Board #Board.objects.all()
	context_object_name = 'boards'#context['boards'] = boards
	template_name = 'boards/index.html' #template = 'boards/index.html'




# def board_topics(request,pk):

# 	context = dict()
# 	board = get_object_or_404(Board,id = pk)
# 	queryset = board.topics.annotate(replies = Count('posts') - 1)# (-1)exclude starter topics
# 	# print(queryset)

# 	# Pagination 

# 	page = request.GET.get('page',1)
# 	paginator = Paginator(queryset,10)#show X items per page

# 	try:
# 		topics = paginator.page(page)
# 	except PageNotAnInteger:
# 		#fallback to first page
# 		topics = paginator.page(1)
# 	except EmptyPage:
# 		#probabily user tries to add a page number in url
# 		#fall back to last page
# 		topics = paginator.page(paginator.num_pages)

# 	# end pagination scripts

# 	template = 'boards/topics.html'
# 	context['board'] = board
# 	context['topics'] = topics
# 	return render(request,template,context)




class BoardTopicsListView(ListView):

	model = Topic #Model to work on
	context_object_name = 'topics' #context['topics'] = topics
	template_name = 'boards/topics.html'
	paginate_by = 5


	def get_context_data(self,**kwargs):
		"""
		overrides context
		"""
		kwargs['board'] = self.board #context['board'] = board
		return super().get_context_data(**kwargs)


	def get_queryset(self):
		"""
		overrides queryset
		"""
		self.board = get_object_or_404(Board,pk=self.kwargs.get('pk'))
		queryset = self.board.topics.annotate(replies = Count('posts') - 1)
		return queryset












@login_required
def new_topic(request,pk):

	current_user = request.user

	context = dict()
	board = get_object_or_404(Board,id = pk)
	form =  NewTopicForm()
	if request.method == 'POST':
		form =  NewTopicForm(data = request.POST)
		if form.is_valid():
			topic_instance = form.save(commit=False)
			topic_instance.board = board
			topic_instance.starter = current_user
			topic_instance.save()

			post,_ = Post.objects.get_or_create(message = request.POST.get('message'),
				topic = topic_instance,
				created_by = current_user)
			return redirect('boards:board_topics',pk = board.pk)
		else:
			pass
			
	template = 'boards/new_topic.html'	
	context['board'] = board
	context['form'] = form
	return render(request,template,context)





# def topic_posts_view(request,board_pk,topic_pk):

# 	context  = dict()
# 	topic = get_object_or_404(Topic,id = topic_pk,board__id = board_pk)
# 	topic.views += 1
# 	topic.save()

# 	template = 'boards/topic_posts.html'
# 	context['topic'] = topic
# 	return render(request,template,context)
	

class TopicPostListView(ListView):

	model = Post
	context_object_name = 'posts'
	template_name = 'boards/topic_posts.html'
	paginate_by = 5


	def get_context_data(self,**kwargs):

		#Views counter for post details -- sweeet !!!
		session_key = 'viewed_topic_{}'.format(self.topic.pk)
		#check if post_id exists in session
		if not self.request.session.get(session_key,False):
			self.topic.views += 1
			self.topic.save() 
			self.request.session[session_key] = True # set user session post id to True (remember it)

		kwargs['topic'] = self.topic
		return super().get_context_data(**kwargs)


	def get_queryset(self):
		self.topic = get_object_or_404(Topic,
			board__pk=self.kwargs.get('board_pk'),
			pk=self.kwargs.get('topic_pk'))

		queryset = self.topic.posts.order_by('-created')
		return queryset







@login_required
def reply_topic(request,board_pk,topic_pk):
    topic = get_object_or_404(Topic,id = topic_pk,board__id = board_pk)
    if request.method == 'POST':
        form = PostForm(data = request.POST)
        if form.is_valid():
            post_instance = form.save(commit=False)
            post_instance.topic = topic
            post_instance.created_by = request.user
            post_instance.save()

            topic.update = timezone.now()
            topic.save()
            # Bug - Fix it !
            return redirect('boards:topic_posts', 
            	board_pk = str(board_pk),
            	topic_pk = str(topic_pk))

        else:
        	pass
    else:
        form = PostForm()
    return render(request, 'boards/reply_topic.html',{'topic': topic, 'form': form})





@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):

	model = Post #model to perform action on
	fields = ('message',)#field to update in the model - (tuple,)
	template_name = 'boards/edit_post.html' #templete render page
	pk_url_kwarg = 'post_pk' # Post instance pk (to edit) ie. update_view(request,post_pk):pass
	context_object_name = 'post' # same as context = {'post':instance}


	def get_queryset(self):
		queryset = super().get_queryset() #override parent queryset that return Post.object.all()
		current_user = self.request.user
		user_only_post = queryset.filter(created_by = current_user)
		return user_only_post



	def form_valid(self,form):
		"""
		handling form validation - dev.
		"""
		post = form.save(commit = False)
		post.updated_by = self.request.user
		post.save()
		return redirect('boards:topic_posts', 
            	board_pk = post.topic.board.pk,
            	topic_pk = post.topic.pk)


