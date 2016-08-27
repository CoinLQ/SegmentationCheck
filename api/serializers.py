from managerawdata.models import OPage
from rest_framework import serializers
from catalogue.models import Tripitaka, Volume
from segmentation.models import Page


class OPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OPage
        fields = ('id', 'tripitaka','volume', 'page_no','page_type','height', 'width',
            'image')

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'text', 'is_correct')

class VolumeSerializer(serializers.ModelSerializer):
    o_pages = OPageSerializer(many=True, read_only=True)
    bars_count = serializers.CharField(read_only=True, source="tripitaka.bars_count")
    class Meta:
        model = Volume
        fields = ('id', 'number','start_page','end_page','o_pages', 'bars_count')

class TripitakaSerializer(serializers.ModelSerializer):
    volumes = VolumeSerializer(many=True, read_only=True)
    class Meta:
        model = Tripitaka
        fields = ('id', 'name','code', 'volumes_count', 'bars_count', 'volumes')
