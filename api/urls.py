from django.conf.urls import include, url
from . import views
from rest_framework import routers

from rest_framework.routers import DefaultRouter
from .views import TripitakaViewSet, VolumeViewSet, OPageViewSet, PageViewSet, CharacterViewSet,CharacterStatisticsViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'tripitaka', TripitakaViewSet)
router.register(r'volume', VolumeViewSet)
router.register(r'o_page', OPageViewSet)
router.register(r'page', PageViewSet)
router.register(r'character', CharacterViewSet)
router.register(r'characterstatistics', CharacterStatisticsViewSet)
urlpatterns = router.urls

