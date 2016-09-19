from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import generics,filters

from .serializers import PageSerializer, OPageSerializer, TripitakaSerializer, VolumeSerializer,CharacterSerializer,CharacterStatisticsSerializer

from managerawdata.models import OPage
from catalogue.models import Tripitaka, Volume
from segmentation.models import Page, Character,CharacterStatistics
from django.contrib.auth import get_user_model

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    search_fields = ('first_name', 'last_name', 'email')
    filter_fields = ('id', 'first_name', 'last_name', 'email')


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


class CharacterViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    queryset = Character.objects.all()
    filter_fields = ('page_id', 'char', 'is_correct')


class CharacterStatisticsViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterStatisticsSerializer
    queryset = CharacterStatistics.objects.all()


class DashBoardViewSet(generics.ListAPIView):

    def list(self, request):
        tripitaka_count = Tripitaka.objects.count()
        done_num = OPage.objects.filter(status=0).count()
        user_total = User.objects.count()
        pending_page = Page.objects.filter(state=-1).count()
        done_page = Page.objects.filter(state=1).count()

        return Response({
                'tripitaka': { 'count': tripitaka_count,
                                'items': TripitakaSerializer(Tripitaka.objects.all().order_by('id'), many=True).data },
                'opage': { 'total': OPage.objects.count(),
                            'done_num': done_num },
                'page': { 'pending': pending_page,
                          'approved': done_page,
                          'count': Page.objects.count() },
                'user': { 'count': User.objects.count() }
        })


