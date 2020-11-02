from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			group=None
			if request.user.groups.exists():
				group= request.user.groups.all()[0].name

			if group == 'Customer':
				return redirect('#')
			# if group== 'Doctor':
			# 	return redirect('doc')
			# if group=='Receptionist':
			# 	return redirect('reception')
			# if group =='human_resource':
			# 	return redirect('human_resource')
			
		else:
			return view_func(request, *args, **kwargs)
	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			group=None
			if request.user.groups.exists():
				group=request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('you are not authorised to view this')
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_func(request, *args, **kwargs):
		group=None
		if request.user.groups.exists():
			group= request.user.groups.all()[0].name

		if group == 'Patient':
			return redirect('pat')
		if group== 'Doctor':
			return redirect('doc')
		if group=='Receptionist':
			return redirect('reception')
		if group =='human_resource':
			return redirect('human_resource')
		
		if group=='admin':
			return view_func(request, *args, **kwargs)
	return wrapper_func
def patient_only(view_func):
	def wrapper_func(request, *args, **kwargs):
		group=None
		if request.user.groups.exists():
			group=request.user.groups.all()[0].name
		if group=='Patient':
			return view_func(request,*args,**kwargs)
	return wrapper_func