from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create$', views.quiz_batch_create, name='quiz_batch_create'),
    url(r'^(?P<batch_id>[0-9]+)/characters$', views.quiz_batch_characters, name='quiz_batch_characters'),
    url(r'^(?P<batch_id>[0-9]+)/$', views.set_correct, name='quiz_batch_set_correct'),
]
