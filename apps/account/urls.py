from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views
from django.contrib import admin
from django.contrib import auth
admin.autodiscover()

urlpatterns = [
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}),
    url('', include('django.contrib.auth.urls')),
    url(r'^register/$', views.register),
]
