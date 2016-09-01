from django.db import models
from catalogue.models import Volume
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Text(models.Model):
    display = models.CharField(max_length=16)
    semanteme = models.ForeignKey("self", blank=True, related_name="Text")
    is_base = models.BooleanField(default=False)

    def __unicode__(self):
        return self.display


# Create your models here.
class Page(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    image = models.CharField(max_length=512)
    volume = models.ForeignKey(Volume, related_name='pages', blank=True, null=True)
    image_upload = models.ImageField(upload_to = 'page_images',max_length=512,null=True)
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
        return settings.PAGE_IMAGE_ROOT+self.image


class Character(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    page = models.ForeignKey(Page)
    text = models.ForeignKey(Text, blank=True, null=True)
    char = models.CharField(max_length=4, db_index=True)
    image = models.CharField(max_length=512)
    #image = models.ImageField(upload_to = 'character_images',max_length=512,null=True)
    left = models.SmallIntegerField()
    right = models.SmallIntegerField()
    top = models.SmallIntegerField()
    bottom = models.SmallIntegerField()
    line_no = models.SmallIntegerField()
    char_no = models.SmallIntegerField()
    region_no = models.SmallIntegerField(default=0)
    is_correct = models.SmallIntegerField(default=0,db_index=True)
#is_correct value
## 0 unchecked(initial value )
## 1 correct
## 2 manual correct
## -1 erro
## -2 with/height erro
## -3 line erro
## -4 page  erro
    #verification_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return u'%s:%s' % (self.id, self.char)

class CharacterStatistics(models.Model):
    char = models.CharField(max_length=4,db_index=True,primary_key=True)
    total_cnt = models.IntegerField(default=0)
    uncheck_cnt = models.IntegerField(default=0)
    err_cnt = models.IntegerField(default=0)
    uncertainty_cnt = models.IntegerField(default=0)


    def __unicode__(self):
        return u'%s:%d' % (self.char,self.total_cnt )

