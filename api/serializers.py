from managerawdata.models import OPage
from rest_framework import serializers
from catalogue.models import Tripitaka, Volume
from segmentation.models import Page,Character,CharacterStatistics
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'last_login',
            'is_active', 'date_joined'
        )

class OPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OPage
        fields = ('id', 'description', 'tripitaka','volume', 'page_no','page_type','height', 'width', 'image','status','image_url')

class VolumeSerializer(serializers.ModelSerializer):
    #o_pages = serializers.SerializerMethodField(read_only=True)
    bars_count = serializers.IntegerField(read_only=True, source="tripitaka.bars_count")
    o_pages_count = serializers.IntegerField(source='get_o_pages_count')
    #v_owner = serializers.SerializerMethodField(read_only=True)
    owner = serializers.SerializerMethodField(source='get_owner', read_only=True)

    def get_o_pages(self, volume):
        qs = OPage.objects.filter(status=0, volume=volume).order_by('-id')
        serializer = OPageSerializer(instance=qs, many=True, read_only=True)
        return serializer.data

    def get_owner(self,volume):
        serializer = UserSerializer(instance=(volume.owner and volume.owner.user), read_only=True)
        return serializer.data

    class Meta:
        model = Volume
        fields = ('id', 'number','start_page','end_page', 'bars_count', 'o_pages_count', 'updated_at',
        'owner', 'completed_count', 'state')#, 'o_pages')
        read_only_fields = ('o_pages_count', 'owner')

class TripitakaSerializer(serializers.ModelSerializer):
    #volumes = VolumeSerializer(many=True, read_only=True)
    class Meta:
        model = Tripitaka
        fields = ('id', 'name','code', 'volumes_count', 'bars_count', 'completed_count', 'completed_volume_ids')#, 'volumes')

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'text', 'is_correct','image','width','height','image_url')


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('id','page', 'char','image', 'is_correct','image_url')

class CharacterStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterStatistics
        fields = ('char','total_cnt', 'uncheck_cnt','err_cnt', 'uncertainty_cnt')
