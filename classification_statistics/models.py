from django.db import models

# Create your models here.
class DataPoint(models.Model):
    char = models.CharField(max_length=4, db_index=True)
    range_idx = models.SmallIntegerField()
    count = models.IntegerField(default=0)
