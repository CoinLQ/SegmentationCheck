# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Tripitaka(models.Model):
    name = models.CharField(max_length=64, verbose_name = _('Tripitaka|name'))
    code = models.CharField(max_length = 10,verbose_name = _('Tripitaka|code'))
    product = models.CharField(max_length=64,verbose_name = _('Tripitaka|product'))
    product_date = models.DateField(verbose_name = _('Tripitaka|product_date'))
    description = models.TextField(verbose_name = _('Tripitaka|description'))
    cover = models.ImageField(upload_to = 'cover', verbose_name= _('Tripitaka|cover'))
    volumes_count = models.SmallIntegerField(default=0, verbose_name = _('Tripitaka|volumes_count'))
    reel_nm = models.SmallIntegerField(default=0, verbose_name = _('Tripitaka|reel_nm'))

    def __unicode__(self):
         return self.name

    class Meta:
        verbose_name = _('tripitaka')
        verbose_name_plural = _('tripitakas')
# che (morden mode)
class Volume(models.Model):
    tripitaka = models.ForeignKey(Tripitaka, null=False, related_name='volumes', verbose_name = _('Volume|tripitaka'))
    sn = models.CharField(max_length=12, default='', verbose_name = _('Volume|sn'))
    pages_nm = models.SmallIntegerField(default=0,verbose_name = _('Volume|pages_nm'))
    start_page = models.SmallIntegerField(default=1, verbose_name = _('Volume|start_page'))
    end_page = models.SmallIntegerField(default=0, verbose_name = _('Volume|end_page'))
    sutras = ArrayField(models.CharField(max_length=134), blank=True, default=[])

    @classmethod
    def format_volume(cls, tripitaka, number):
        return '{0}-TV{1:04}'.format(tripitaka.code, number)

    def get_o_pages_count(self):
        return self.o_pages.filter(volume=self).count()

    class Meta:
        verbose_name = _('Segmentation|volume')
        verbose_name_plural = _('Segmentation|volumes')

    def __unicode__(self):
        return u'%s %s' % (self.tripitaka.name, self.sn)

# juan (ancient mode)
class Reel(models.Model):
    tripitaka = models.ForeignKey(Tripitaka, null=False, related_name='reels', verbose_name = _('tripitaka'))
    sn = models.CharField(max_length=12, default='')
    pages_count = models.SmallIntegerField(default=0,verbose_name = _('Reel|pages_count'))
    sutras = ArrayField(models.CharField(max_length=134), blank=True)

class NormalizeSutra(models.Model):
    sn = models.CharField(max_length=12, default='')
    name = models.CharField(max_length=128, default='', primary_key=True)
    era = models.CharField(max_length=12, default='')
    discription = models.TextField(default='')

    def __unicode__(self):
        return self.name

class Sutra(models.Model):
    id = models.CharField(max_length=12, default='', primary_key=True)
    tripitaka = models.ForeignKey(Tripitaka)
    normal_sutra = models.ForeignKey(NormalizeSutra,null=True)
    name = models.CharField(max_length=128, default='')
    era = models.CharField(max_length=12, default='')
    translator = models.CharField(max_length=64, default='')
    # 译经之前的原始卷数
    reel_nm = models.SmallIntegerField(default=0, verbose_name = _('reel_nm'))

    start_page = models.CharField(max_length=12, default='', verbose_name = _('Sutra|start_page'))
    end_page = models.CharField(max_length=12, default='', verbose_name = _('Sutra|end_page'))
    discription = models.CharField(max_length=512, default='')

    @classmethod
    def format_sutra(cls, tripitaka, number):
        return '{0}-TS{1:04}'.format(tripitaka.code, number)

    def __unicode__(self):
         return self.name
