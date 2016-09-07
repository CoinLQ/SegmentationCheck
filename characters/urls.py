from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='character_index'),
    url(r'^task/$', views.task, name='task'),
    url(r'^set_correct$', views.set_correct, name='set_correct'),
]
