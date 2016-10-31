from django.conf.urls import include, url
from . import views
from rest_framework import routers

from rest_framework.routers import DefaultRouter
from views.default import TripitakaViewSet, VolumeViewSet, OPageViewSet, \
  PageViewSet, CharacterStatisticsViewSet, DataPointViewSet

from views.character_view import CharacterViewSet
from django.conf.urls import url, patterns, include


character_cut = CharacterViewSet.as_view({'get': 'cut_detail','post': 'apply_cut'})
character_cut_list = CharacterViewSet.as_view({'get': 'cut_list'})

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'tripitaka', TripitakaViewSet)
router.register(r'volume', VolumeViewSet)
router.register(r'o_page', OPageViewSet)
router.register(r'page', PageViewSet)
router.register(r'character', CharacterViewSet)
router.register(r'characterstatistics', CharacterStatisticsViewSet)
router.register(r'datapoint', DataPointViewSet)

urlpatterns = patterns(
  '',
  url(r'^', include(router.urls)),
  url(r'^character/(?P<pk>[0-9A-Za-z-]+)/direct/(?P<direct>[a-z-]+)/cut$', character_cut_list, name='character_cut_list'),
  url(r'^character/(?P<pk>[0-9A-Za-z-]+)/direct/(?P<direct>[a-z-]+)/cut/(?P<image_no>[1-5-]+)$', character_cut, name='character_cut'),
)