from django.conf.urls import include, url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #url('^', include('django.contrib.auth.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^demo/$', views.demo, name='demo'),
    url(r'^login/$', auth_views.login, {'template_name':'login.html'},name='login'),
    url(r'^logout/$', auth_views.logout,{'template_name':'logout.html'},name='logout'),
    url(r'^pagecheck/(?P<pk>[0-9A-Za-z]*)$', views.PageCheckView.as_view(), name='page_check'),
    url(r'^set_page_correct$', views.set_page_correct, name='set_page_correct'),
    url(r'^characterindex/$', views.CharacterIndex.as_view(), name='character_index'),
    url(r'^charactercheck/(?P<char>.*)', views.character_check, name='character_check'),
    url(r'^set_correct$', views.set_correct, name='set_correct'),
    url(r'^errpageindex/$', views.ErrPageIndex.as_view(), name='err_page_index'),
    url(r'^run_segment/(?P<page_id>[0-9A-Za-z]+)$', views.runSegment, name='run_segment'),
    url(r'^(?P<page_id>[0-9A-Za-z]+)/$', views.page_detail, name='page_detail'),
    url(r'^(?P<page_id>[0-9A-Za-z]+)/modify$', views.page_modify, name='page_modify'),
    url(r'^(?P<page_id>[0-9A-Za-z]+)/segmentation_line$', views.page_segmentation_line, name='page_segmentation_line'),
]
