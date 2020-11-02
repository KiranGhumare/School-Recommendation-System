from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import CustomerForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user,allowed_users,admin_only

def home(request):
	return render(request, 'sch/index.html')
def contact(request):
	return render(request, 'sch/contact.html')
def register(request):
	
	form= CreateUserForm()
	if request.method=='POST':
		form= CreateUserForm(request.POST)
		if form.is_valid():
			
			user= form.save()
			Customer.objects.create(user=user,)
			group = Group.objects.get(name='Customer')
			user.groups.add(group)
			username=form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + username)


			return redirect('login')
	context={'form':form}
	return render(request, 'sch/register.html',context)

def loginpage(request):
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user= authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			if request.user.groups.exists():
				group= request.user.groups.all()[0].name
			if group =='Customer':
				return redirect('home')
			# if group=='Doctor':
			# 	return redirect('doc')
			# if group=='Receptionist':
			# 	return redirect('reception')
			# if group=='human_resource':
			# 	return redirect('human_resource')
			# if group=='admin':
			# 	return redirect('#')
			
		else:
			messages.info(request,'Username OR password is incorrect')
	return render(request, 'sch/login.html')

def about(request):
	return render(request, 'sch/about.html')