from django.conf.urls import include, url
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required


from . import views

urlpatterns = [
  url(r'sutras$', login_required(views.SutraList.as_view()), name='sutra_index'),
  url(r'sutras/(?P<pk>([0-9a-zA-Z-]+)$)', views.SutraDetail.as_view(), name='sutra_detail'),
]
