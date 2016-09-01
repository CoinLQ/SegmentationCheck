from django.conf.urls import include, url
from . import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
#===segment modify
    url(r'^errpageindex/$', views.ErrPageIndex.as_view(), name='err_page_index'),
    url(r'^run_segment/(?P<page_id>[0-9A-Za-z-]+)$', views.runSegment, name='run_segment'),
    url(r'^(?P<page_id>[0-9A-Za-z]+)/$', views.page_detail, name='page_detail'),
    url(r'^(?P<page_id>[0-9A-Za-z]+)/modify$', views.page_modify, name='page_modify'),
]
