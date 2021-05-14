from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from django.contrib.gis import forms

from django import forms
# from .models import Location


# class LocationForm(forms.ModelForm):
#
#     class Meta:
#
#         model = Location
#         fields = '__all__'


class FilterForm(forms.Form):
	ty1 = forms.CheckboxSelectMultiple()
	ty2 = forms.CheckboxSelectMultiple()
	ty3 = forms.CheckboxSelectMultiple()
	ty4 = forms.CheckboxSelectMultiple()
	ty5 = forms.CheckboxSelectMultiple()
	ty6 = forms.CheckboxSelectMultiple()
	ty7 = forms.CheckboxSelectMultiple()
	ty8 = forms.CheckboxSelectMultiple()
	ty9 = forms.CheckboxSelectMultiple()
	ty10 = forms.CheckboxSelectMultiple()
	ty11 = forms.CheckboxSelectMultiple()

	

    # ty1 = forms.CheckboxInput(check_test=None)
    # ty2 = forms.CheckboxInput(check_test=None)
    # ty3 = forms.CheckboxInput(check_test=None)
    # ty4 = forms.CheckboxInput(check_test=None)
    # ty5 = forms.CheckboxInput(check_test=None)
    # ty6 = forms.CheckboxInput(check_test=None)
    # ty7 = forms.CheckboxInput(check_test=None)
    # ty8 = forms.CheckboxInput(check_test=None)
    # ty9 = forms.CheckboxInput(check_test=None)
    # ty10 = forms.CheckboxInput(check_test=None)
    # ty11 = forms.CheckboxInput(check_test=None)


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['first_name','last_name','username','email','password1','password2']


class CustomerForm(ModelForm):
    class Meta:
	    model = Customer
	    fields = '__all__'
	    exclude= ['user']



class NearMeForm(ModelForm):
    # location = forms.PointField()
    class Meta:
        model = Customer
        fields = ['location']
