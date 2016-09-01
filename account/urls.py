from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name':'login.html'},name='login'),
    url(r'^logout/$', auth_views.logout,{'template_name':'logout.html'},name='logout'),
]
