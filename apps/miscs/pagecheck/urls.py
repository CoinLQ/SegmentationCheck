from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<pk>[0-9A-Za-z-]*)$', views.PageCheckView.as_view(), name='page_check'),
    url(r'^set_page_correct$', views.set_page_correct, name='set_page_correct'),
]
