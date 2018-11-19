from django.db import models
import re
from datetime import datetime
import bcrypt

NAME_REGEX = re.compile(r'^[a-zA-Z ]*$')

class UserManager(models.Manager):
	def register_validator(self, postData):
		errors = {}

		if len(postData['username']) < 3:
			errors['username'] = "Username should be at least 3 characters."
		elif User.objects.filter(username=postData['username']):
			errors['username'] = "Username is already taken."

		if len(postData['password']) < 8:
			errors['password'] = "Password should be at least 8 characters."
		elif postData['password'] != postData['confirm']:
			errors['password'] = "Password does not match."

		if len(postData['name']) < 3:
			errors['name'] = "Name should be at least 3 characters."
		elif not NAME_REGEX.match(postData['name']):
			errors['name'] = "Not a valid name."

		return errors

	def login_validator(self, postData):
		errors = {}

		if len(postData['passwordlogin']) < 1:
			errors['passwordlogin'] = "Password cannot be blank."

		if len(postData['usernamelogin']) < 1:
			errors['usernamelogin'] = "Username cannot be blank."
		elif not User.objects.filter(username=postData['usernamelogin']):
			errors['usernamelogin'] = "Username is not in database."

		else:
			user = User.objects.filter(username=postData['usernamelogin'])
			print(user)
			if not bcrypt.checkpw(postData['passwordlogin'].encode(), user[0].password.encode()):
				errors['passwordlogin'] = "Passwords don't match"

		return errors

class TripManager(models.Manager):
	def trip_validator(self, postData):
		errors = {}

		if not postData['destination']:
			errors['title'] = "Destination cannot be blank."
		if not postData['description']:
			errors['description'] = "Description cannot be blank."
		
		if not postData['startdate']:
			errors['startdate'] = "Start date cannot be blank."
		elif postData['startdate'] < str(datetime.now()):
			errors['startdate'] = "Star Date cannot be a past date."

		if not postData['enddate']:
			errors['enddate'] = "End date cannot be blank."
		elif postData['enddate'] < str(datetime.now()):
			errors['enddate'] = "End date cannot be a past date."

		if postData['startdate'] > postData['enddate']:
			errors['startdate'] = "Star Date cannot be after end date."
			
		return errors

class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	# favorited_movies (Many to many)
	# uploaded_movies (One to many)
	objects = UserManager()

class Trip(models.Model):
	destination = models.CharField(max_length=255)
	description = models.TextField(max_length=1000)
	startdate = models.DateTimeField()
	enddate = models.DateTimeField()
	joined_users = models.ManyToManyField(User, related_name="joined_trips")
	uploader = models.ForeignKey(User, related_name="uploaded_trip", on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = TripManager()
