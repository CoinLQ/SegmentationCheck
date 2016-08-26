from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from .serializers import PageSerializer, OPageSerializer, TripitakaSerializer
from managerawdata.models import OPage
from catalogue.models import Tripitaka, Volume
from segmentation.models import Page
from rest_framework.response import Response


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    def update(self, request, pk=None):
        instance = Page.objects.get(pk=pk)
        instance.text = request.data['text']
        instance.save()
        serializer = PageSerializer(instance)
        return Response(serializer.data)

class OPageViewSet(viewsets.ModelViewSet):
    serializer_class = OPageSerializer
    queryset = OPage.objects.all()
    search_fields = ('pages_no', 'tripitaka')


class TripitakaViewSet(viewsets.ModelViewSet):
    serializer_class = TripitakaSerializer
    queryset = Tripitaka.objects.all()