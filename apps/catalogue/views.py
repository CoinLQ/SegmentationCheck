from django.shortcuts import render
from django.views import generic

from .models import Sutra
# Create your views here.

class SutraList(generic.ListView):
    template_name = 'sutras/index.html'
    context_object_name = 'sutra_list'

    def get_queryset(self):
        from segmentation.models import Page
        #Page.rebuild_accuracy()
        sutra_list = Sutra.objects.all().order_by('id')
        return  sutra_list


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SutraList, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        #context['book_list'] = Book.objects.all()
        return context

class SutraDetail(generic.DetailView):
    template_name = 'sutras/detail.html'
    model = Sutra

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SutraDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        #context['book_list'] = Book.objects.all()
        return context