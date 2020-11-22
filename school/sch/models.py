from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
	GENDER=(('Male', 'Male'),
		('Female','Female'),
		('Other','Other')
		)
	user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=200, null=True)
	last_name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created= models.DateTimeField(auto_now_add=True, null=True)
	phone = models.CharField(max_length=12, null=True)
	gender = models.CharField(max_length=100,null=True, choices=GENDER)
	age= models.CharField(max_length=200, null=True)
	profile_pic=models.ImageField(default="profile_aBGztjN.png",null=True,blank=True)
	# ap=models.ForeignKey(app_of_Patient,null=True,on_delete=SET_NULL)
	
	def __str__(self):
		return self.user.username

class School_info(models.Model):
	
	school_name=models.CharField(max_length=1000,null=True)
	gender_allowed=models.CharField(max_length=1000,null=True)
	type_school=models.CharField(max_length=1000,null=True)
	board=models.CharField(max_length=1000,null=True)
	fees=models.CharField(max_length=1000,null=True)
	grade=models.CharField(max_length=1000,null=True)
	min_age=models.CharField(max_length=1000,null=True)
	medium=models.CharField(max_length=1000,null=True)
	avg_class_strength=models.CharField(max_length=1000,null=True)
	estd=models.CharField(max_length=1000,null=True)
	school_strength=models.CharField(max_length=1000,null=True)
	swimming_pool=models.CharField(max_length=1000,null=True)
	indoor_sports=models.CharField(max_length=1000,null=True)
	ac_classes=models.CharField(max_length=1000,null=True)
	transportation=models.CharField(max_length=1000,null=True)
	outdoor_sports=models.CharField(max_length=1000,null=True)
	annual_fees=models.CharField(max_length=1000,null=True)
	admission_fees=models.CharField(max_length=1000,null=True)
	phone1=models.CharField(max_length=1000,null=True)
	phone2=models.CharField(max_length=1000,null=True)
	phone3=models.CharField(max_length=1000,null=True)
	phone4=models.CharField(max_length=1000,null=True)
	address=models.CharField(max_length=1000,null=True)


	def __str__(self):
		return self.school_name
		
class Contact(models.Model):
	name=models.CharField(max_length=300, null=True)
	email=models.CharField(max_length=300, null=True)
	phone=models.CharField(max_length=20, null=True)
	desc=models.CharField(max_length=1000, null=True)
	
	def __str__(self):
		return self.name

class gender(models.Model):
	name=models.CharField(max_length=300,null=True)

	def __str__(self):
		return self.name


class Board_allowed(models.Model):
	name=models.CharField(max_length=300,null=True)

	def __str__(self):
		return self.name

class Facility(models.Model):
	name=models.CharField(max_length=300,null=True)

	def __str__(self):
		return self.name
