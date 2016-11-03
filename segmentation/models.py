from django.db import models
from catalogue.models import Volume
from managerawdata.models import OPage
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.cache import cache
import math
import random
from skimage import io
import os
import shutil
from PIL import Image
from utils.qiniu_uploader import upload_file


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
        return settings.PAGE_IMAGE_ROOT+self.image

    @property
    def image_url(self):
        return '/dzj_characters/page_images'+self.image


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
    ## the field values. [1, 0, -1]. 1 means correct, -1 not, 0 default
    is_correct = models.SmallIntegerField(default=0, db_index=True)
    ## the field values. [1, 0, -1]. 1 means integrity, -1 not, 0 default
    is_integrity = models.SmallIntegerField(default=0, db_index=True)
    accuracy = models.SmallIntegerField(default=-1, db_index=True)

    class Meta:
        index_together = [
            ("char", "is_correct"),
        ]

    def __unicode__(self):
        return u'%s:%s' % (self.id, self.char)

    def resource_key(self):
        modified_time = 0
        try:
            statbuf = os.stat(self.get_image_path())
            modified_time = statbuf.st_mtime
        except:
            pass
        return self.page_id+u'/'+self.image.replace(u'.jpg', u'.png') + ("?v=%d" % modified_time)

    @property
    def image_url(self):
        url = cache.get('ch_url' + self.id, None)
        if url is not None:
            return url
        server_host = "http://asset-c%d.dzj3000.com" % int(math.ceil(random.random()*1))
        return server_host + '/web/character_images/' +self.resource_key()
        # return u'/character_images/'+self.page_id+u'/'+self.image.replace(u'.jpg', u'.png')

    def local_image_url(self):
        statbuf = os.stat(self.get_image_path())
        return u'/character_images/'+self.page_id+u'/'+self.image +  ("?v=%d" % statbuf.st_mtime)

    def get_image_path(self):
        base_path = settings.CHARACTER_IMAGE_ROOT+self.page_id
        if not os.access(base_path, os.X_OK):
            os.mkdir(base_path)
        return settings.CHARACTER_IMAGE_ROOT+self.page_id+u'/'+self.image

    def get_cut_image_path(self):
        base_path = settings.CUT_CHARACTER_IMAGE_ROOT+self.page_id
        if not os.access(base_path, os.X_OK):
            os.mkdir(base_path)
        image_path = self.resource_key()
        return settings.CUT_CHARACTER_IMAGE_ROOT + image_path


    def danger_rebuild_image(self):
        pageimg_file = self.page.get_image_path()
        page_image = io.imread(pageimg_file, 0)
        char_image = page_image[self.top:self.bottom, self.left:self.right]
        io.imsave(self.get_image_path(), char_image)

    def upload_png_to_qiniu(self):
        png_filename = self.get_image_path().replace('.jpg', '.png')
        image_file = Image.open(self.get_image_path())
        #image_file = image_file.convert('1')
        image_file.save(png_filename)
        return upload_file(png_filename, self.resource_key())

    def backup_orig_character(self):
        new_file = self.get_cut_image_path()
        shutil.copy(self.get_image_path(), new_file)
        return new_file

    def image_tag(self):
        return u'<img src="%s" border="1" style="zoom: 20%%;" />' % (self.image_url)
    image_tag.short_description = u'Image'
    image_tag.allow_tags = True

class CharacterStatistics(models.Model):
    char = models.CharField(max_length=4,db_index=True,primary_key=True)
    total_cnt = models.IntegerField(default=0)
    uncheck_cnt = models.IntegerField(default=0)
    err_cnt = models.IntegerField(default=0)
    correct_cnt = models.IntegerField(default=0)
    weight = models.DecimalField(default=0, max_digits=4, decimal_places=3, db_index= True)

    def __unicode__(self):
        return u'%s:%d' % (self.char,self.total_cnt )
