from django.db import models
from catalogue.models import Tripitaka,Volume
from django.core.serializers.json import DjangoJSONEncoder
import json

class MyJsonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, OPage):
            return {
                u'id': obj.id,
                u'tripitaka': obj.tripitaka.name,
                u'volume': obj.volume.number,
                u'pages_no': obj.pages_no,
                u'image_url': obj.image.url,
                u'width': obj.width,
                u'height': obj.height,
            }
        return super(MyJsonEncoder, self).default(obj)



class OPage(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    tripitaka = models.ForeignKey(Tripitaka)
    volume = models.ForeignKey(Volume)
    pages_no = models.SmallIntegerField()
    image = models.ImageField(upload_to = 'opage_images',max_length=512,null=True)
    width = models.SmallIntegerField()
    height = models.SmallIntegerField()

    def json_serialize(self):
        return json.dumps(self,cls=MyJsonEncoder)

