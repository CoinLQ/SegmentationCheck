from managerawdata.models import OPage
from rest_framework import serializers
from catalogue.models import Tripitaka, Volume


class OPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OPage
        fields = ('id', 'tripitaka','volume', 'pages_no', 'height', 'width',
            'image')


class VolumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volume
        fields = ('id', 'number')

class TripitakaSerializer(serializers.ModelSerializer):
    volumes = VolumeSerializer(many=True, read_only=True)
    class Meta:
        model = Tripitaka
        fields = ('id', 'name','code', 'volumes_count', 'bars_count', 'volumes')