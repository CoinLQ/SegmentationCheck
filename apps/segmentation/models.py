import math
import os
import random
import shutil
import logging
import urllib2
import json
import base64

from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models, transaction
from django.db.models import SmallIntegerField,Sum, Case, When, Value, Count, Avg
from django.utils.translation import ugettext_lazy as _

from PIL import Image
from skimage import io
from utils.qiniu_uploader import upload_file

from catalogue.models import Volume, Sutra
from managerawdata.models import OPage
from libs.thumbnail import ThumbnailMixin
from libs.storage import silentremove

from libs.classifier import pred_process

logger = logging.getLogger(__name__)
# Create your models here.
class Page(models.Model, ThumbnailMixin):

    id = models.CharField(max_length=32, primary_key=True)
    image = models.CharField(max_length=512)
    volume = models.ForeignKey(Volume, related_name='pages', blank=True, null=True)
    o_page = models.ForeignKey(OPage, related_name='pages', blank=True, null=True)
    sutra = models.ForeignKey(Sutra, related_name='pages', blank=True, null=True)
    text = models.TextField()
    width = models.SmallIntegerField(default=0)
    height = models.SmallIntegerField(default=0)
    left = models.SmallIntegerField(default=0)
    right = models.SmallIntegerField(default=0)
    ## the field values. [1, 0, -1]. 1 means correct, -1 not, 0 default
    is_correct = models.SmallIntegerField(default=0)
    accuracy = models.IntegerField(default=0)

    def __unicode__(self):
        return self.id

    def short_text(self):
        s_text = u''
        start_pos = self.text.find(u';')
        pos = self.text.find(u'\n')
        if start_pos != -1:
            s_text = self.text[start_pos + 1:pos].strip()
        return s_text

    @staticmethod
    def rebuild_accuracy():
        pages_avg = cache.get("pages_avg", None)
        if not pages_avg:
            pages_avg = Character.objects.filter(is_correct=1).values('page_id').order_by().annotate(avg=Avg('accuracy'))
            cache.set("pages_avg", pages_avg)
            pages = []
            for i, page in enumerate(pages_avg, start=1):
                pages.append(page)
                if i % 5000 == 0:
                    with transaction.atomic():
                        for page in pages:
                            dp = Page.objects.get(pk=page['page_id'])
                            dp.accuracy = page['avg']
                            dp.save()
                    pages = []
            with transaction.atomic():
                for page in pages:
                    dp = Page.objects.get(pk=page['page_id'])
                    dp.accuracy = page['avg']
                    dp.save()

    @property
    def gaolizang_id(self):
        return self.id[8:]

    @property
    def thumbnail_image_url(self):
        return self.get_thumbnail_url()

    @property
    def summary(self):
        ret = {}
        if not self.text:
            return ret
        lines = self.text.replace('\r\n','\n').split(u'\n')
        for line in lines:
            if len(line)==0:
                continue
            if ';' in line:
                key, value = line.split(';')
                ret[key.strip()]=value.strip()
        return ret

    def locate_char(self, character):
        try:
            word = self.summary[character.line_no_text][character.char_pos-1]
        except KeyError, e:
            logger.error("not found %s in %s" % (character.line_no_text, self.id))
            word='NAN'
        return word

    def get_image_path(self):
        return settings.PAGE_IMAGE_ROOT + self.id + '.jpg'

    @property
    def image_url(self):
        return '/page_images/'+self.image


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
    ## the field values. [1, 0, -1]. 1 means same, -1 not, 0 default
    is_same = models.SmallIntegerField(default=0)
    accuracy = models.SmallIntegerField(default=-1, db_index=True)
    is_dirty = models.BooleanField(default=False)
    recog_chars = ArrayField(models.CharField(max_length=4, blank=True), size=10, default=[])


    class Meta:
        index_together = [
            ("char", "is_correct"),
            ("char", "accuracy"),
            ("char", "is_same"),
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
        server_host = "http://dzj3000.lqdzj.cn" % int(math.ceil(random.random() * 1))
        return server_host + '/web/character_images/' + self.resource_key().replace(u'.jpg', u'.png')

    @property
    def rect(self):
        return [self.left, self.top, self.right-self.left, self.bottom - self.top]

    @property
    def line_no_text(self):
        return self.id.split('L')[0]+"L"

    @property
    def line_no(self):
        return int(self.id.split('L')[0][-2:])

    @property
    def char_pos(self):
        return int(self.id.split('L')[1])

    def local_image_url(self):
        try:
            statbuf = os.stat(self.get_image_path())
        except:
            statbuf = timezone.now()
        return u'/character_images/'+self.page_id+u'/'+self.image +  ("?v=%d" % statbuf.st_mtime)

    def get_image_path(self):
        base_path = settings.CHARACTER_IMAGE_ROOT+self.page_id
        image_path = settings.CHARACTER_IMAGE_ROOT+self.page_id+u'/'+self.image
        if not os.access(image_path, os.X_OK):
            if not os.access(base_path, os.X_OK):
                os.mkdir(base_path)
            self.danger_rebuild_image()
        return image_path

    def get_cut_image_path(self):
        base_path = settings.CUT_CHARACTER_IMAGE_ROOT+self.page_id
        if not os.access(base_path, os.X_OK):
            os.mkdir(base_path)
        image_path = self.resource_key()
        return settings.CUT_CHARACTER_IMAGE_ROOT + image_path

    def danger_rebuild_image(self):
        try:
            pageimg_file = self.page.get_image_path()
            page_image = io.imread(pageimg_file, 0)
            char_image = page_image[self.top:self.bottom, self.left:self.right]
            image_path = settings.CHARACTER_IMAGE_ROOT+self.page_id+u'/'+self.image
            io.imsave(image_path, char_image)
        except IOError, e:
            pass
        #silentremove(self.npy_path())

    def upload_png_to_qiniu(self):
        png_filename = self.png_path()
        image_file = Image.open(self.get_image_path())
        image_file.save(png_filename)
        qiniu_key = 'web/character_images/' + self.page_id+u'/'+self.image.replace(u'.jpg', u'.png')
        # return upload_file(png_filename, qiniu_key)
        return 'qiniu disabled'

    def backup_orig_character(self):
        backup_file = self.get_cut_image_path()
        try:
            shutil.copy(self.get_image_path(), backup_file)
        except:
            pass
        return backup_file

    def base64_jpg(self):
        try:
            f = open( self.get_image_path(), 'rb')
            img64 = base64.b64encode(f.read())
            f.close()
        except:
            img64 = '/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAVACQDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+iiigAooooAKKKKACiiigAooooAKKKKAP//Z'
        return img64

    def predict_reg(self):
        host = 'http://www.dzj3000.lqdzj.cn:9090'
        params = { "images": [self.base64_jpg()] }
        req = urllib2.Request(host + "/imglst")
        req.add_header("Content-Type", "application/json")
        response = urllib2.urlopen(req, json.dumps(params))
        ret = json.loads(response.read())
        if (self.char == ret['predictions'][0][0]):
            self.is_same = 1
        else:
            self.is_same = -1
        self.recog_chars = ret['predictions'][0]
        self.save()
        return ret['predictions'][0]

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
            total_cnt=Count('is_correct'),
            recog_diff_count=Sum(Case(When(is_correct=-1, is_same=1, then=Value(1)), When(is_correct=1, is_same=-1, then=Value(1)),
            default=Value(0),
            output_field=SmallIntegerField())))
        # add character statistics, if it's missing.
        statistics, created = CharacterStatistics.objects.get_or_create(char=char)
        CharacterStatistics.objects.filter(char=char).update(uncheck_cnt=result['uncheck_cnt'], correct_cnt=result['correct_cnt'],
                        err_cnt=result['err_cnt'], total_cnt=result['total_cnt'], recog_diff_count=result['recog_diff_count'])

    @classmethod
    def recog_characters(cls, char):
        import time
        char_count_map = {}
        total_count = Character.objects.filter(char=char, is_same=0).count()
        iter_count = (total_count - 1) / 100
        start = 0
        left_count = total_count % 100
        for i in range(iter_count):
            start = i * 100
            characters = Character.objects.filter(char=char, is_same=0)[0:100]
            Character.bulk_update_recog_2(characters)
            print(i)
            time.sleep(1)
        characters = Character.objects.filter(char=char, is_same=0)[start:left_count]
        Character.bulk_update_recog_2(characters)

    @classmethod
    @transaction.atomic
    def bulk_update_recog(cls, char_list):
        if not char_list:
               return
        host = 'http://www.dzj3000.lqdzj.cn:9090'
        image_list = map(lambda ch:ch.base64_jpg(), char_list)
        params = { "images": image_list }
        req = urllib2.Request(host + "/imglst")
        req.add_header("Content-Type", "application/json")
        response = urllib2.urlopen(req, json.dumps(params))
        ret = json.loads(response.read())
        recog_result = ret['predictions']
        for index, ch in enumerate(char_list):
            if (ch.char == recog_result[index][0]):
                ch.is_same = 1
            else:
                ch.is_same = -1
            ch.recog_chars = recog_result[index]
            ch.save()

    @classmethod
    @transaction.atomic
    def bulk_update_recog_2(cls, char_list):
        if not char_list:
               return
        image_list = map(lambda ch:ch.get_image_path(), char_list)
        ret = pred_process.process(image_list)
        recog_result = ret['predictions']
        for index, ch in enumerate(char_list):
            if (ch.char == recog_result[index][0]):
                ch.is_same = 1
            else:
                ch.is_same = -1
            ch.recog_chars = recog_result[index]
            ch.save()

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

    def reformat_self(self, direct):
        if 't' in direct:
            char = self.up_neighbor_char()
            char.bottom = self.top
        else:
            char = self.down_neighbor_char()
            char.top = self.bottom

        backup_file = char.backup_orig_character()
        char.danger_rebuild_image()
        char.is_integrity = 1
        char.is_correct = 0
        try:
            char.predict_reg()
        except:
            pass
        char.save()
        return char, backup_file

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
    recog_diff_count = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s:%d' % (self.char,self.total_cnt )
