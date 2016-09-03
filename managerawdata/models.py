# -*- coding: utf-8 -*-
from django.db import models
from catalogue.models import Tripitaka,Volume
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from PIL import Image



class OPage(models.Model):
    id = models.CharField(max_length=32,primary_key = True )
    tripitaka = models.ForeignKey(Tripitaka)
    volume = models.ForeignKey(Volume, related_name='o_pages')
    page_no = models.SmallIntegerField(default = 0)
    page_type = models.SmallIntegerField(default =1 ) #1single 2 dual
    image = models.ImageField(upload_to = 'opage_images',max_length=512,null=True,blank=True)
    width = models.SmallIntegerField(default =0 )
    height = models.SmallIntegerField(default = 0)
    status = models.SmallIntegerField(default = 0) #0 inital 1:output page


    @property
    def description(self):
        return u"%s 第%s册 第%s页" % (self.tripitaka.name, self.volume.number, self.page_no)

    def __unicode__(self):
         return self.id

    class Meta:
        verbose_name = _('opage')
        verbose_name_plural = _('opages')

    def get_image_path(self):
        return '/opage_images/'+self.image

@receiver(pre_save, sender=OPage)
def my_handler(sender, instance, **kwargs):
    # initial image size info
    img = Image.open(instance.image.path)
    instance.width = img.width
    instance.height = img.height
