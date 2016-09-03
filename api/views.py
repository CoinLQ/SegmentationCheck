from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, mixins
from .serializers import PageSerializer, OPageSerializer, TripitakaSerializer, VolumeSerializer
from managerawdata.models import OPage
from catalogue.models import Tripitaka, Volume
from segmentation.models import Page
from rest_framework.response import Response
from rest_framework import generics,filters
from libs.pagination import StandardPagination


class PageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PageSerializer
    pagination_class = StandardPagination
    queryset = Page.objects.all()
    filter_fields = ('id', 'text', 'volume')

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
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('status','id','volume')


class TripitakaViewSet(viewsets.ModelViewSet):
    serializer_class = TripitakaSerializer
    queryset = Tripitaka.objects.all()


class VolumeViewSet(viewsets.ModelViewSet):
    serializer_class = VolumeSerializer
    queryset = Volume.objects.all()

