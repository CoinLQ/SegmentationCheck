from django.db import models
from catalogue.models import Tripitaka,Volume
from django.utils.translation import ugettext_lazy as _
#from django.core.serializers.json import DjangoJSONEncoder
#import json
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from PIL import Image



#class MyJsonEncoder(DjangoJSONEncoder):
#    def default(self, obj):
#        if isinstance(obj, OPage):
#            return {
#                u'id': obj.id,
#                u'tripitaka': obj.tripitaka.name,
#                u'volume': obj.volume.number,
#                u'pages_no': obj.pages_no,
#                u'image_url': obj.image.url,
#                u'width': obj.width,
#                u'height': obj.height,
#            }
#        return super(MyJsonEncoder, self).default(obj)



class OPage(models.Model):
    id = models.CharField(max_length=32,primary_key = True )
    tripitaka = models.ForeignKey(Tripitaka)
    volume = models.ForeignKey(Volume)
    pages_no = models.SmallIntegerField(default = 0)
    image = models.ImageField(upload_to = 'opage_images',max_length=512,null=True,blank=True)
    width = models.SmallIntegerField(default =0 )
    height = models.SmallIntegerField(default = 0)

    def __unicode__(self):
         return self.id

    class Meta:
        verbose_name = _('opage')
        verbose_name_plural = _('opages')

#    def json_serialize(self):
#        return json.dumps(self,cls=MyJsonEncoder)



@receiver(pre_save, sender=OPage)
def my_handler(sender, instance, **kwargs):
    # initial image size info
    img = Image.open(instance.image.path)
    instance.width = img.width
    instance.height = img.height
