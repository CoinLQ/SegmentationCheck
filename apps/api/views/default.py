from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import generics, filters

from api.serializers import PageSerializer, OPageSerializer, TripitakaSerializer, VolumeSerializer, \
    CharacterSerializer,CharacterStatisticsSerializer, DataPointSerializer

from classification_statistics.models import DataPoint

from managerawdata.models import OPage
from catalogue.models import Tripitaka, Volume
from segmentation.models import Page, Character, CharacterStatistics
from rest_framework.filters import DjangoFilterBackend, OrderingFilter
from rest_framework.decorators import detail_route


class TripitakaViewSet(viewsets.ModelViewSet):
    serializer_class = TripitakaSerializer
    queryset = Tripitaka.objects.all()

class VolumeViewSet(viewsets.ModelViewSet):
    serializer_class = VolumeSerializer
    queryset = Volume.objects.all()

class OPageViewSet(viewsets.ModelViewSet):
    serializer_class = OPageSerializer
    queryset = OPage.objects.all()
    search_fields = ('pages_no', 'tripitaka')
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('status', 'id', 'volume')

class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()#.order_by('accuracy')
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    #filter_backends = (filters.OrderingFilter,)
    filter_fields = ('is_correct', 'id', 'volume', 'sutra')

    @detail_route(methods=['put'], url_path='mark_is_correct')
    def mark_is_correct(self, request, pk=None):
        instance = Page.objects.get(pk=pk)
        instance.is_correct = request.data['is_correct']
        instance.save()
        serializer = PageSerializer(instance)
        return Response(serializer.data)

    @detail_route(methods=['post'], url_path='toggle_correct')
    def toggle_correct(self, request, pk):
        instance = Page.objects.get(pk=pk)
        if (instance.is_correct != 1):
            instance.is_correct = 1
        else:
            instance.is_correct = -1
        instance.save()
        serializer = PageSerializer(instance)
        return Response(serializer.data)

class CharacterStatisticsViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterStatisticsSerializer
    queryset = CharacterStatistics.objects.all().order_by('-total_cnt', 'char')
    filter_fields = ('char', )

class DataPointViewSet(viewsets.ModelViewSet):
    serializer_class = DataPointSerializer
    filter_fields = ('char', )
    paginator = None
    queryset = DataPoint.objects.order_by('range_idx')

