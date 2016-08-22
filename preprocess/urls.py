from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.PreprocessIndex.as_view(), name='preprocess_index'),
    url(r'^cut/(?P<bookpage_id>[0-9A-Za-z-]+)$', views.bookpage_cut, name='bookpage_cut'),
]
