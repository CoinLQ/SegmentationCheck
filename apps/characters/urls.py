from django.conf.urls import include, url
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from . import views

urlpatterns = [
    #url(r'^$', views.index, name='character_index'),
    url(r'^$', login_required(views.Index.as_view()), name='character_index'),
    url(r'^list/$', login_required(views.List .as_view()), name='character_list'),
    url(r'^task/$', views.task, name='task'),
    url(r'^task/help$', views.help, name='help'),
    url(r'^set_correct$', views.set_correct, name='set_correct'),
    url(r'^treemap$', views.tree_map),
    url(r'^dashboard$', views.char_dashboard),
    url(r'^stackedareachart$', views.stacked_area_chart),
    url(r'^get_marked_char_count$', views.get_marked_char_count, name='get_marked_char_count'),
    url(r'^classify$', views.classify, name='classify'),
    url(r'^accuracy_count$', views.accuracy_count, name='accuracy_count'),
    url(r'^marked_by_accuracy$', views.marked_by_accuracy, name='marked_by_accuracy'),
    url(r'^demo$', views.recog_demo, name='recog_demo'),
    url(r'^last_task_result$', views.last_task_result, name='last_task_result'),
    url(r'^more_task_result$', views.more_task_result, name='more_task_result'),
    url(r'^(?P<character_id>[0-9A-Za-z-]+)$', views.detail, name='character_detail'),
    #url(r'^readonly/(?P<char>(.*))$', views.readonly, name='character_readonly'),
    url(r'^(?P<char>(.*))$', views.browser, name='character_browser'),

]
