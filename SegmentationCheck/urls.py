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

urlpatterns = [
    url(r'^$', home.views.index, name='main_index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^app/', home.views.app, name='app'),
    url(r'^account/', include('account.urls',namespace='account')),
    url(r'^home/', include('home.urls',namespace='home')),
    url(r'^managerawdata/', include('managerawdata.urls',namespace='managerawdata')),
    url(r'^preprocess/', include('preprocess.urls',namespace='preprocess')),
    url(r'^segmentation/', include('segmentation.urls',namespace='segmentation')),
    url(r'^layoutseg/', include('layoutseg.urls',namespace='layoutseg')),
    url(r'^charseg/', include('charseg.urls',namespace='charseg')),
    url(r'^characters/', include('characters.urls',namespace='characters')),
    url(r'^pagecheck/', include('pagecheck.urls',namespace='pagecheck')),
    url(r'^api/', include('api.urls',namespace='api')),
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
    ]
