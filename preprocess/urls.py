from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.PreprocessIndex.as_view(), name='preprocess_index'),
    url(r'^opage_cut$', views.opage_cut, name='opage_cut'),
    url(r'^text_process/(?P<page_id>[0-9A-Za-z-]+)$', views.text_process, name='text_process'),
]
