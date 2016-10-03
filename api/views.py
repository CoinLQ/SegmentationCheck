from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import generics, filters

from .serializers import PageSerializer, OPageSerializer, TripitakaSerializer, VolumeSerializer,CharacterSerializer,CharacterStatisticsSerializer

from managerawdata.models import OPage
from catalogue.models import Tripitaka, Volume
from segmentation.models import Page, Character, CharacterStatistics


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
            'accuracy': ['lt', 'gt'],
            'page_id': ['exact'],
            'char': ['exact'],
            'is_correct': ['exact', 'lt', 'gt'],
        }

class CharacterViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    filter_class = CharacterFilter
    queryset = Character.objects.order_by('accuracy')

class CharacterStatisticsViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterStatisticsSerializer
    queryset = CharacterStatistics.objects.all().order_by('-total_cnt')
    filter_fields = ('char', )
