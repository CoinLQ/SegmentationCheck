from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.PreprocessIndex.as_view(), name='preprocess_index'),
    url(r'^opage_cut/(?P<opage_id>[0-9A-Za-z-]+)$', views.opage_cut, name='opage_cut'),
]
