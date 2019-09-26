
from django.contrib.auth import views as auth_views #built-in auth.
from django.urls import path
from .import views

app_name = 'account'

urlpatterns = [
    path('register/',views.signup,name='sign-up'),
    path('login/',auth_views.LoginView.as_view(template_name='account/login.html'), name='sign-in'),
    path('logout/',auth_views.LogoutView.as_view(),name='sign-out'),
    path('update/user/',views.UserUpdateView.as_view(),name='update_account'),
    # ajax validation - username
    path('server-side/validate/username/',views.validate_username,name='validate_username'),
    # password reset,change route
    path('reset/',auth_views.PasswordResetView.as_view(
    	template_name='account/password_reset.html',
    	email_template_name='account/password_reset_email.html',
    	subject_template_name='account/password_reset_subject.txt'),
    name = 'password_reset'),

    path('reset/done/',auth_views.PasswordResetDoneView.as_view(
    	template_name='account/password_reset_done.html'),
    name = 'password_reset_done'),

    path('reset/<str:uidb64>/<str:token>/',auth_views.PasswordResetConfirmView.as_view(
    	template_name='account/password_reset_confirm.html'),
    name = 'password_reset_confirm'),

    path('reset/complete/',auth_views.PasswordResetCompleteView.as_view(
    	template_name='account/password_reset_complete.html'),
    name = 'password_reset_complete'),

]
