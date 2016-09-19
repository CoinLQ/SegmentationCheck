from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
from account.models import UserProfile


# Create your models here.
class Tripitaka(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('Tripitaka|name'))
    code = models.CharField(max_length=10, verbose_name=_('Tripitaka|code'))
    product = models.CharField(max_length=128, verbose_name=_('Tripitaka|product'))
    product_date = models.DateField(verbose_name=_('Tripitaka|product_date'))
    description = models.TextField(verbose_name=_('Tripitaka|description'))
    cover = models.ImageField(upload_to='cover', verbose_name=_('Tripitaka|cover'))
    volumes_count = models.SmallIntegerField(default=0, verbose_name=_('Tripitaka|volumes_count'))
    bars_count = models.SmallIntegerField(default=0, verbose_name=_('Tripitaka|bars_count'))
    default_bars = JSONField(default=[(100, 60, 1250, 1020), (80, 1050, 1250, 2000)])
    completed_count =  models.SmallIntegerField(default=0, verbose_name=_('Tripitaka|completed_count'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('tripitaka')
        verbose_name_plural = _('tripitakas')


class Volume(models.Model):
    tripitaka = models.ForeignKey(Tripitaka, null=False, related_name='volumes', verbose_name=_('Volume|tripitaka'))
    number = models.SmallIntegerField(verbose_name=_('Volume|number'))
    pages_count = models.SmallIntegerField(default=0, verbose_name=_('Volume|pages_count'))
    start_page = models.SmallIntegerField(default=0, verbose_name=_('Volume|start_page'))
    end_page = models.SmallIntegerField(default=0, verbose_name=_('Volume|end_page'))
    owner = models.ForeignKey(UserProfile, related_name='volumes', null=True)

    def get_o_pages_count(self):
        return self.o_pages.filter(volume=self).count()

    class Meta:
        verbose_name = _('Segmentation|volume')
        verbose_name_plural = _('Segmentation|volumes')

    def __unicode__(self):
        return u'%s %s' % (self.tripitaka.name, self.number)


class NormalizeSutra(models.Model):
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=64)
    discription = models.TextField()

    def __unicode__(self):
        return self.name


class Sutra(models.Model):
    tripitaka = models.ForeignKey(Tripitaka)
    norma_sutra = models.ForeignKey(NormalizeSutra)
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=64)
    discription = models.CharField(max_length=512)
    start = models.CharField(max_length=32)
    end = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name
