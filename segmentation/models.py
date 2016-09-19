#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from catalogue.models import Volume
from managerawdata.models import OPage
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import datetime
from libs.thumbnail import ThumbnailMixin
# Create your models here.
class Page(models.Model, ThumbnailMixin):
    id = models.CharField(max_length=32, primary_key=True)
    image = models.CharField(max_length=512)
    volume = models.ForeignKey(Volume, related_name='pages', blank=True, null=True)
    o_page = models.ForeignKey(OPage, related_name='pages', blank=True, null=True)
    text = models.TextField()
    width = models.SmallIntegerField(default=0)
    height = models.SmallIntegerField(default=0)
    left = models.SmallIntegerField(default=0)
    right = models.SmallIntegerField(default=0)
    state = models.SmallIntegerField(default=0)
    erro_char_cnt = models.IntegerField(default=0)

#state value
## 0 unchecked(initial value )
## 1 correct
## -1 pending
## -2 text error

    @staticmethod
    def correct_page_count():
        return Page.objects.all().filter(state=1).count()

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
        #return 'http://ob21oo6fl.bkt.clouddn.com/page_images/'+self.image

    @property
    def image_url(self):
        return '/page_images/' + self.image
        #return 'http://ob21oo6fl.bkt.clouddn.com/page_images/'+self.image


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

    @property
    def image_url(self):
        return '/character_images/'+self.page_id+'/'+self.image


class CharacterStatistics(models.Model):
    char = models.CharField(max_length=4,db_index=True,primary_key=True)
    total_cnt = models.IntegerField(default=0)
    uncheck_cnt = models.IntegerField(default=0)
    err_cnt = models.IntegerField(default=0)
    uncertainty_cnt = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s:%d' % (self.char,self.total_cnt )

class PageComment(models.Model):
    STATE_CHOICES = (
        ('PE', '待处理'),
        ('DN', '已处理'),
        ('RJ', '已拒绝'),
        ('AP', '已接受'),
    )
    comment = models.CharField(max_length=128, blank=False)
    page = models.OneToOneField(Page, related_name='page_comment')
    collator = models.ForeignKey(User, blank=True, related_name='comments')
    admin = models.ForeignKey(User, blank=True, related_name='answers')
    reply = models.CharField(max_length=128, blank=True)
    comment_at = models.DateTimeField(default=datetime.now, blank=True)
    replay_at = models.DateTimeField(blank=True)
    state =models.CharField(max_length=2,
        choices=STATE_CHOICES,
        default='PE')
