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
def category(request):
	return render(request, 'sch/category.html')
def category_gender(request,gender_name):
    gens=gender.objects.all()
    boards=Board_allowed.objects.all()
    items=School_info.objects.all()
    facs=Facility.objects.all()
    print(request.GET)
    gend=request.GET.get('ty')

    if gend=="Co-Ed School" or gend=="Only Boys School" or gend=="Only Girls School":
    	tys=items.filter(gender_allowed=gend)
    	return render(request, 'sch/category.html',{'gens':gens,'tys':tys,'boards':boards,'facs':facs})
    elif gend=="CBSE" or gend=="IGCSE" or gend=="IB" or gend=="State Board" or gend=="ICSE":
    	tys=items.filter(board=gend)
    	return render(request, 'sch/category.html',{'gens':gens,'tys':tys,'boards':boards,'facs':facs})
    elif gend=="AC Classrooms" or gend=="Transportation" or gend=="Swimming Pool":
    	if(gend=="AC Classrooms"):
    		tys=items.filter(ac_classes="Yes ")
    		print(tys)
    	elif gend=="Transportation":
    		tys=items.filter(transportation="Yes ")
    	elif gend=="Swimming Pool":
    		tys=items.filter(swimming_pool="Yes ")
    	return render(request, 'sch/category.html',{'gens':gens,'tys':tys,'boards':boards,'facs':facs})

    return render(request, 'sch/category.html', {'items':items,'gens':gens,'boards':boards,'facs':facs})

def category(request):
    gens=gender.objects.all()
    items = School_info.objects.all()
    boards=Board_allowed.objects.all()
    facs=Facility.objects.all()
    return render(request, 'sch/category.html', {'items':items,'gens':gens,'boards':boards,'facs':facs})

def school_page(request,pk):
	item= School_info.objects.get(id=pk)
	
	return render(request,'sch/school_page.html',{'item':item})

