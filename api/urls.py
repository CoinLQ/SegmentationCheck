from django.conf.urls import include, url
from . import views
from rest_framework import routers

from rest_framework.routers import DefaultRouter
from .views import PreprocessViewSet

router = routers.SimpleRouter(trailing_slash=True)
router.register(r'opage', PreprocessViewSet)
urlpatterns = router.urls

