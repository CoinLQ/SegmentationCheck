from django.shortcuts import render

from rest_framework import viewsets
from .serializers import PreprocessSerializer
from managerawdata.models import OPage


class PreprocessViewSet(viewsets.ModelViewSet):
    serializer_class = PreprocessSerializer
    queryset = OPage.objects.all()
    search_fields = ('pages_no', 'tripitaka')

