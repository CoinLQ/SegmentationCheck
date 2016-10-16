from django.shortcuts import render
from django.views import generic
# Create your views here.
class Index(generic.ListView):
  template_name = 'charts.html'
  def get_queryset(self):
    return []

  def index(request):
    return render(request, 'charts.html')
