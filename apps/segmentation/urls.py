from django.conf.urls import include, url
from . import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
#===segment modify
    url(r'^(?P<page_id>[0-9A-Za-z-]+)/$', views.page_detail, name='page_detail'),
  #  url(r'^(?P<page_id>[0-9A-Za-z-]+)/dirty$', views.page_dirty, name='page_modify'),
]
