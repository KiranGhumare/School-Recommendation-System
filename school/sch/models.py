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


# class Doctor(models.Model):
# 	STATUS=(('Active','Active'),('Inactive','Inactive'))
# 	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
# 	first_name = models.CharField(max_length=200, null=True)
# 	last_name = models.CharField(max_length=200, null=True)
# 	email = models.CharField(max_length=200, null=True)
# 	date_created= models.DateTimeField(auto_now_add=True, null=True)
# 	patient = models.ForeignKey(Patient, null=True, on_delete=models.SET_NULL)
# 	profile_pic=models.ImageField(default="profile_aBGztjN.png",null=True,blank=True)
# 	status = models.CharField(max_length=200, null=True, choices=STATUS)
# 	dept=models.CharField(max_length=300,null=True)
	
# 	def __str__(self):
# 		return self.user.username



# class Appointment(models.Model):
# 	STATUS = (
# 			('Pending', 'Pending'),
# 			('Completed', 'Completed')
# 			)
# 	patient = models.ForeignKey(Patient, null=True, on_delete=models.SET_NULL)
# 	doctor = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL)
# 	date_created = models.DateTimeField(auto_now_add=True, null=True)
# 	status = models.CharField(max_length=200, null=True, choices=STATUS) 


# # class app_of_Patient(models.Model):
# # 	appo=models.ForeignKey(Appointments, null=True, on_delete=models.SET_NULL)

# class Prescription(models.Model):
# 	patient= models.ForeignKey(Patient, null=True, on_delete=models.SET_NULL)
# 	doctor=models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL)
# 	date_created=models.DateTimeField(auto_now_add=True,null=True)
# 	prescri=models.CharField(max_length=1000, null=True)
# 	symptoms=models.CharField(max_length=1000, null=True)
	




# class Contact(models.Model):
# 	name=models.CharField(max_length=300, null=True)
# 	email=models.CharField(max_length=300, null=True)
# 	phone=models.CharField(max_length=20, null=True)
# 	desc=models.CharField(max_length=1000, null=True)