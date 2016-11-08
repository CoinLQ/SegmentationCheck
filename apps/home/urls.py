from django.conf.urls import include, url
from . import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^demo/$', views.demo),
    url(r'^joinus/$', views.join_us),
]
