
from django.contrib import admin
from django.urls import path
from account import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from .views import settings, change_password, failed, change_profile_picture, success


urlpatterns= [
	path('signup/', views.signUpUser, name='signup'),
	path('login/', views.loginUser, name='login'),
	path('logout/', views.logoutUser, name='logout'),
    path('settings/', settings, name='settings'),
    path('change_password/', change_password, name='change_password'),
    path('change_profile_picture/', change_profile_picture, name='change_profile_picture'),
    path('failed/', failed, name='failed'),
    path('success/', success, name='success'),
]

