from django.conf.urls import url
from . import views           

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^dash$', views.dash),
	url(r'^clear$', views.clear),
	url(r'^new$', views.new),
	url(r'^create$', views.create),
	url(r'^join/(?P<tripid>\d+)$', views.join),
	url(r'^show/(?P<tripid>\d+)$', views.show),
]