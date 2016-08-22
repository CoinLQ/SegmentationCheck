from django.conf.urls import include, url
from . import views
from rest_framework import routers

from rest_framework.routers import DefaultRouter
from .views import PreprocessViewSet

router = routers.SimpleRouter(trailing_slash=True)
router.register(r'cut', PreprocessViewSet)
urlpatterns = router.urls


urlpatterns += [
    url(r'^$', views.PreprocessIndex.as_view(), name='preprocess_index'),
    #url(r'^cut/(?P<bookpage_id>[0-9A-Za-z-]+)$', views.bookpage_cut, name='bookpage_cut'),
]