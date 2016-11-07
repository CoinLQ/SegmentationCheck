import math
import os
import random
import shutil
import logging

from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import SmallIntegerField,Sum, Case, When, Value, Count
from django.utils.translation import ugettext_lazy as _

from PIL import Image
from skimage import io
from utils.qiniu_uploader import upload_file

from catalogue.models import Volume
from managerawdata.models import OPage

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
    ## the field values. [1, 0, -1]. 1 means correct, -1 not, 0 default
    is_correct = models.SmallIntegerField(default=0)
    erro_char_cnt = models.IntegerField(default=0)

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
        return '/dzj_characters/page_images/'+self.image


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
            ("char", "accuracy"),
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
        return self.page_id + u'/' + self.image + ("?v=%d" % modified_time)

    def npy_path(self):
        _path = 'npy/character_images/%s/%s.nln.npy' % (self.page_id, self.id)
        return settings.CHARACTER_IMAGE_ROOT + _path

    def png_path(self):
        _path = 'png/character_images/%s/%s.png' % (self.page_id, self.id)
        return settings.CHARACTER_IMAGE_ROOT + _path

    @property
    def image_url(self):
        url = cache.get('ch_url' + self.id, None)
        if url is not None:
            return url

        if self.is_integrity == 1:
            return self.local_image_url()
        server_host = "http://asset-c%d.dzj3000.com" % int(math.ceil(random.random() * 1))
        return server_host + '/web/character_images/' + self.resource_key().replace(u'.jpg', u'.png')

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
        png_filename = self.png_path()
        image_file = Image.open(self.get_image_path())
        image_file.save(png_filename)
        qiniu_key = 'web/character_images/' + self.page_id+u'/'+self.image.replace(u'.jpg', u'.png')
        # return upload_file(png_filename, qiniu_key)
        return 'qiniu disabled'

    def backup_orig_character(self):
        new_file = self.get_cut_image_path()
        shutil.copy(self.get_image_path(), new_file)
        return new_file

    @classmethod
    def update_statistics(cls, char):
        result = Character.objects.filter(char=char).aggregate(
            correct_cnt=Sum(Case(When(is_correct=1, then=Value(1)),
            default=Value(0),
            output_field=SmallIntegerField())),
            err_cnt=Sum(Case(When(is_correct=-1, then=Value(1)),
            default=Value(0),
            output_field=SmallIntegerField())),
            uncheck_cnt=Sum(Case(When(is_correct=0, then=Value(1)),
            default=Value(0),
            output_field=SmallIntegerField())),
            total_cnt=Count('is_correct') )
        # add character statistics, if it's missing.
        statistics, created = CharacterStatistics.objects.get_or_create(char=char)
        CharacterStatistics.objects.filter(char=char).update(uncheck_cnt=result['uncheck_cnt'], correct_cnt=result['correct_cnt'],
                        err_cnt=result['err_cnt'], total_cnt=result['total_cnt'])

    def up_neighbor_char(self):
        key_prefix = self.pk.split('L')[0]
        num = int(self.pk.split('L')[1])
        neighbor_key = '{0}L{1:02}'.format(key_prefix, num - 1)
        if not Character.objects.filter(pk=neighbor_key).exists():
            logger = logging.getLogger('char_log')
            logger.info(neighbor_key)
        return Character.objects.get(pk=neighbor_key)

    def down_neighbor_char(self):
        key_prefix = self.pk.split('L')[0]
        num = int(self.pk.split('L')[1])
        neighbor_key = '{0}L{1:02}'.format(key_prefix, num + 1)
        if not Character.objects.filter(pk=neighbor_key).exists():
            logger = logging.getLogger('char_log')
            logger.info(neighbor_key)
        return Character.objects.get(pk=neighbor_key)

    def reformat_self(self):
        up_char = self.up_neighbor_char()
        up_char.bottom = self.top
        up_char.backup_orig_character()
        up_char.is_integrity = 1
        up_char.is_correct = 0
        up_char.save()
        up_char.danger_rebuild_image()
        down_char = self.down_neighbor_char()
        down_char.top = self.bottom
        down_char.backup_orig_character()
        down_char.is_integrity = 1
        down_char.is_correct = 0
        down_char.save()
        down_char.danger_rebuild_image()



    def image_tag(self):
        return u'<img src="%s" border="1" style="zoom: 100%%;" />' % (self.image_url)
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
