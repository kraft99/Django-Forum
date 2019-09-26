from .decorators import ajax_required

from django.contrib import auth
from django.conf import settings
from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .forms import SignUpForm




def signup(request):
	template = 'account/signup.html'
	form = SignUpForm()

	if request.method == 'POST':
		form = SignUpForm(data = request.POST)
		if form.is_valid():
			user_instance = form.save(commit=False)
			user_instance.save()
			auth.login(request,user_instance)
			return redirect('/')
		else:
			pass

	context = {
	'form':form
	}
	return render(request,template,context)



class UserUpdateView(UpdateView):

	model = User
	fields = ('username','email','first_name','last_name')
	template_name = 'account/update_user_account.html'
	success_url = reverse_lazy('account:update_account')#same view


	def get_object(self):
		return self.request.user





# TODO : fix bug
@ajax_required
def validate_username(request):
	requested_username = request.GET.get('username')

	flag = User.objects.filter(username = requested_username).exists()
	response = {
	'is_available':flag
	}
	return JsonResponse(response)