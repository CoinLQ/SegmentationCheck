from django.conf.urls import include, url
from . import views

urlpatterns = [
    #url(r'^$', views.index, name='rawdata_index'),
    url(r'^$', views.OpageIndex.as_view(), name='rawdata_index'),
    url(r'^opage/upload$', views.opage_upload, name='opage_upload'),
]
