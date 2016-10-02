from django.db import models
from catalogue.models import Volume
from managerawdata.models import OPage
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


# Create your models here.
class Page(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    image = models.CharField(max_length=512)
    volume = models.ForeignKey(Volume, related_name='pages', blank=True, null=True)
    o_page = models.ForeignKey(OPage, related_name='pages', blank=True, null=True)
    text = models.TextField()
    width = models.SmallIntegerField(default=0)
    height = models.SmallIntegerField(default=0)
    left = models.SmallIntegerField(default=0)
    right = models.SmallIntegerField(default=0)
    is_correct = models.SmallIntegerField(default=0)
    erro_char_cnt = models.IntegerField(default=0)
#is_correct value
## 0 unchecked(initial value )
## 1 correct
## -1 erro
## -2 Character erro
## -3 line erro
## -4 page  erro

    def __unicode__(self):
        return self.id

    def short_text(self):
        s_text = u''
        start_pos = self.text.find(u';')
        pos = self.text.find(u'\n')
        if start_pos != -1:
            s_text = self.text[start_pos + 1:pos].strip()
        return s_text

    def get_image_path(self):
        #return settings.PAGE_IMAGE_ROOT+self.image
        return 'http://ob21oo6fl.bkt.clouddn.com/page_images/'+self.image

    @property
    def image_url(self):
        return 'http://ob21oo6fl.bkt.clouddn.com/page_images/'+self.image


class Character(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    page = models.ForeignKey(Page)
    char = models.CharField(max_length=4, db_index=True)
    image = models.CharField(max_length=512)
    left = models.SmallIntegerField()
    right = models.SmallIntegerField()
    top = models.SmallIntegerField()
    bottom = models.SmallIntegerField()
    line_no = models.SmallIntegerField()
    char_no = models.SmallIntegerField()
    region_no = models.SmallIntegerField(default=0)
    is_correct = models.SmallIntegerField(default=0,db_index=True)
    accuracy = models.FloatField(default=-1.0, db_index=True)
#is_correct value
## 0 unchecked(initial value )
## 1 correct
## 2 manual correct
## -5
##  5
## -1 erro
## -2 width/height erro
## -3 line erro
## -4 page  erro
## -5 image file does not exists.
## -6 the image is white or black.
    #verification_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return u'%s:%s' % (self.id, self.char)

    @property
    def image_url(self):
        return '/character_images/'+self.page_id+'/'+self.image

    def get_image_path(self):
        return settings.CHARACTER_IMAGE_ROOT+self.page_id+'/'+self.image

    def image_tag(self):
        return u'<img src="%s" />' % (self.image_url)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

class CharacterStatistics(models.Model):
    char = models.CharField(max_length=4,db_index=True,primary_key=True)
    total_cnt = models.IntegerField(default=0)
    uncheck_cnt = models.IntegerField(default=0)
    err_cnt = models.IntegerField(default=0)
    uncertainty_cnt = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s:%d' % (self.char,self.total_cnt )
