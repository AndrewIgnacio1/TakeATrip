from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from .models import User, Trip
import bcrypt


def index(request):
	if 'user_id' in request.session:
		return redirect('/dash')

	else:
		context = {
			"users": User.objects.all(),
		}
		return render(request, "myapp/index.html", context)

def register(request):
	errors = User.objects.register_validator(request.POST)
	request.session["name"] = request.POST["name"]
	request.session["username"] = request.POST["username"]
	print(request.session["name"])
	if len(errors):
		for key, error in errors.items():
			messages.add_message(request, messages.ERROR, error, extra_tags='register')
		return redirect('/')
	else:
		pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		user = User.objects.create(name=request.POST["name"], username=request.POST["username"], password=pwhash.decode('utf-8'))
		request.session["user_id"] = user.id
		return redirect('/dash')

def login(request):
	errors = User.objects.login_validator(request.POST)
	print(errors)
	if len(errors):
		for key, error in errors.items():
			messages.add_message(request, messages.ERROR, error, extra_tags='login')
		return redirect('/')
	else:
		user = User.objects.get(username=request.POST['usernamelogin'])
		request.session['user_id'] = user.id
		print('session id is', request.session['user_id'])
		return redirect('/dash')

def dash(request):
	if 'user_id' not in request.session:
		return redirect('/')
	else:
		other_trips = []
		all_trips = Trip.objects.all()
		mytrips = User.objects.get(id=request.session['user_id']).joined_trips.all()
		for trip in all_trips:
			if trip not in mytrips:
				other_trips.append(trip)
		context = {
			"trips": other_trips,
			"user" : User.objects.get(id=request.session['user_id']),
			"mytrips": mytrips,
		}
		return render(request, "myapp/dash.html", context)

def new(request):
	return render(request, "myapp/new.html")

def create(request):
	errors = Trip.objects.trip_validator(request.POST)
	request.session["destination"] = request.POST["destination"]
	request.session["description"] = request.POST["description"]
	request.session["startdate"] = request.POST["startdate"]
	request.session["enddate"] = request.POST["enddate"]
	if errors:
		for key, error in errors.items():
			messages.add_message(request, messages.ERROR, error)
		print(errors)
		return redirect('/new')
	else:
		trip = Trip.objects.create(destination=request.POST["destination"], description=request.POST["description"], startdate=request.POST["startdate"], enddate=request.POST["enddate"], uploader_id = request.session['user_id'])
		trip.joined_users.add(User.objects.get(id=request.session['user_id']))
		#this is creating the joined 
		return redirect('/dash')

def clear(request):
	request.session.clear()
	return redirect("/")

def join(request, tripid):
	trip = Trip.objects.get(id=tripid)
	trip.joined_users.add(User.objects.get(id=request.session['user_id']))
	return redirect('/dash')

def show(request, tripid):
	trip = Trip.objects.get(id=tripid)
	uploaderid = trip.uploader_id
	joinedusers = trip.joined_users.all()
	
	other_users = []
	for user in joinedusers:
		if user.id != uploaderid:
			other_users.append(user)
	context = {
		"trip": trip,
		"users": trip.joined_users.all(),
		"others": other_users
	}
	return render(request, 'myapp/show.html', context)