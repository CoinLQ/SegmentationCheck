from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import generics, filters

from .serializers import PageSerializer, OPageSerializer, TripitakaSerializer, VolumeSerializer, \
    CharacterSerializer,CharacterStatisticsSerializer, DataPointSerializer

from classification_statistics.models import DataPoint

from managerawdata.models import OPage
from catalogue.models import Tripitaka, Volume
from segmentation.models import Page, Character, CharacterStatistics
from libs.count_helper import ApproxCountPgQuerySet

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


class PageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    filter_fields = ('id', 'text', 'volume')

    def update(self, request, pk=None):
        instance = Page.objects.get(pk=pk)
        instance.text = request.data['text']
        instance.save()
        serializer = PageSerializer(instance)
        return Response(serializer.data)

class CharacterFilter(filters.FilterSet):
    class Meta:
        model = Character
        fields = {
            'accuracy': ['lt', 'gt', 'lte', 'gte'],
            'page_id': ['exact'],
            'char': ['exact'],
            'is_correct': ['exact', 'lt', 'gt'],
        }

class CharacterViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    filter_class = CharacterFilter
    #qs = Character.objects.order_by('accuracy')
    #queryset = qs._clone(klass=ApproxCountPgQuerySet)
    queryset = Character.objects.order_by('accuracy')

    #queryset = Character.objects.filter(is_correct__lt=2).\
    #    filter(is_correct__gt=-2).order_by('accuracy')

class CharacterStatisticsViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterStatisticsSerializer
    queryset = CharacterStatistics.objects.all().order_by('-total_cnt', 'char')
    filter_fields = ('char', )

class DataPointViewSet(viewsets.ModelViewSet):
    serializer_class = DataPointSerializer
    filter_fields = ('char', )
    paginator = None
    queryset = DataPoint.objects.order_by('range_idx')

