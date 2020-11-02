from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns= [
	path('',views.home,name="home"),
	path('register/', views.register, name="register"),
	path('contact/', views.contact, name="contact"),
	path('about/', views.about, name="about"),
	path('login/', views.loginpage, name="login"),
]