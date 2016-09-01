from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^characterindex/$', views.CharacterIndex.as_view(), name='character_index'),
    url(r'^characters/$', views.CharacterIndex.as_view(), name='character_index'),
    url(r'^charactercheck/(?P<char>.*)', views.character_check, name='character_check'),
    url(r'^set_correct$', views.set_correct, name='set_correct'),
]
