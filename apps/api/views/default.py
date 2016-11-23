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

    @detail_route(methods=['get'], url_path='split_presets')
    def split_presets(self, request, pk):
        instance = Page.objects.get(pk=pk)
        lines_hash = {}
        results = instance.character_set.order_by('-id')
        if not results.first():
            return Response({'id': instance.id, 'lines_hash': lines_hash})
        for ch in results:
            line_no_text = "%dL" % ch.line_no
            if not lines_hash.get(line_no_text):
                lines_hash[line_no_text] = { "border_r": ch.right,
                    "border_l": ch.left, "char_lst": []}
            lines_hash[line_no_text]["char_lst"].append({
                "bottom": ch.bottom,
                "top": ch.top,
                "char_no": ch.char_pos,
                "char": ch.char
                })
        return Response({'id': instance.id, 'lines_hash': lines_hash})


class CharacterStatisticsViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterStatisticsSerializer
    queryset = CharacterStatistics.objects.all().order_by('-total_cnt', 'char')
    filter_fields = ('char', )

class DataPointViewSet(viewsets.ModelViewSet):
    serializer_class = DataPointSerializer
    filter_fields = ('char', )
    paginator = None
    queryset = DataPoint.objects.order_by('range_idx')

