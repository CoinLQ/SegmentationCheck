"""SegmentationCheck URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
import home.views
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

handler404 = 'home.views.page_not_found'

urlpatterns = [
    url(r'^$', home.views.index, name='main_index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^home/', include('home.urls', namespace='home')),
    url(r'^preprocess/', include('preprocess.urls', namespace='preprocess')),
    url(r'^managerawdata/', include('managerawdata.urls', namespace='managerawdata')),
    url(r'^page/', include('segmentation.urls', namespace='segmentation')),
    url(r'^classification_statistics/', include('classification_statistics.urls', namespace='classification_statistics')),
    url(r'^characters/', include('characters.urls', namespace='characters')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^quiz/', include('quiz.urls', namespace='quiz')),
    url(r'^tripitaka/', include('catalogue.urls', namespace='tripitaka'))
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^cover/(?P<path>.*)$', serve, {
            'document_root': settings.COVER_IMAGE_ROOT,
        }),
        url(r'^opage_images/(?P<path>.*)$', serve, {
            'document_root': settings.OPAGE_IMAGE_ROOT,
        }),
        url(r'^page_images/(?P<path>.*)$', serve, {
            'document_root': settings.PAGE_IMAGE_ROOT,
        }),
        url(r'^character_images/(?P<path>.*)$', serve, {
            'document_root': settings.CHARACTER_IMAGE_ROOT,
        }),
        url(r'^cut_character_images/(?P<path>.*)$', serve, {
            'document_root': settings.CUT_CHARACTER_IMAGE_ROOT,
        }),

    ]
