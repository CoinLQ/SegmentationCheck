from django.conf.urls import include, url
from . import views
from rest_framework import routers

from rest_framework.routers import DefaultRouter
from .views import PageViewSet, OPageViewSet, TripitakaViewSet

router = routers.SimpleRouter(trailing_slash=True)
router.register(r'opage', OPageViewSet)
router.register(r'page', PageViewSet)
router.register(r'tripitaka', TripitakaViewSet)
urlpatterns = router.urls

