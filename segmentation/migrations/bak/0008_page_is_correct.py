# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0007_auto_20160713_0257'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='is_correct',
            field=models.SmallIntegerField(default=0),
        ),
    ]
