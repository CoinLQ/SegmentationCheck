from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from .serializers import OPageSerializer, TripitakaSerializer
from managerawdata.models import OPage
from catalogue.models import Tripitaka, Volume
from rest_framework.response import Response

class OPageViewSet(viewsets.ModelViewSet):
    serializer_class = OPageSerializer
    queryset = OPage.objects.all()
    search_fields = ('pages_no', 'tripitaka')


class TripitakaViewSet(viewsets.ModelViewSet):
    serializer_class = TripitakaSerializer
    queryset = Tripitaka.objects.all()