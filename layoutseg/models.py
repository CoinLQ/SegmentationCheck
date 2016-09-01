from django.db import models
from django.utils.translation import ugettext_lazy as _
from segmentation.models import Page

class Region(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    page = models.ForeignKey(Page)
    text = models.TextField(blank=True,null=True)
    left = models.SmallIntegerField(default=0)
    right = models.SmallIntegerField(default=0)
    top = models.SmallIntegerField(default=0)
    bottom = models.SmallIntegerField(default=0)
    line_no = models.SmallIntegerField(default=0)
    region_no = models.SmallIntegerField(default=0)
    mark = models.CharField(max_length=2,blank=True,null=True)

    def __unicode__(self):
         return self.id

    class Meta:
        verbose_name = _('region')
        verbose_name_plural = _('regions')

    def toJSON(self):
        import json
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))
