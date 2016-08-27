from django.conf.urls import include, url
from . import views
from rest_framework import routers

from rest_framework.routers import DefaultRouter
from .views import PageViewSet, OPageViewSet, TripitakaViewSet, VolumeViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'o_page', OPageViewSet)
router.register(r'page', PageViewSet)
router.register(r'tripitaka', TripitakaViewSet)
router.register(r'volume', VolumeViewSet)
urlpatterns = router.urls

