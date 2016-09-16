from django.conf.urls import include, url
from . import views
from django.contrib.auth.views import login, logout_then_login


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^demo/$', views.demo),
    url(r'^joinus/$', views.join_us),
]
