from django.conf.urls import include, url
from . import views

urlpatterns = [
    #url(r'^$', views.index, name='character_index'),
    url(r'^$', views.Index.as_view(), name='character_index'),
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
    url(r'^last_task_result$', views.last_task_result, name='last_task_result'),
]
