from managerawdata.models import OPage
from rest_framework import serializers


class PreprocessSerializer(serializers.ModelSerializer):
    class Meta:
        model = OPage
        image = serializers.URLField
        fields = ('id', 'tripitaka','volume', 'pages_no', 'height', 'width',
            'image')
