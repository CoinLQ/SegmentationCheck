from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'tripitaka_create', views.TripitakaCreate.as_view(), name='tripitaka_create'),
    url(r'tripitaka_update/(?P<pk>[0-9A-Za-z-]+)$', views.TripitakaUpdate.as_view(), name='tripitaka_update'),
    url(r'tripitaka_delete/(?P<pk>[0-9A-Za-z-]+)$', views.TripitakaDelete.as_view(), name='tripitaka_delete'),
    url(r'volume/(?P<pk>[0-9A-Za-z-]+)$', views.VolumeIndex.as_view(), name='volume_index'),
]
