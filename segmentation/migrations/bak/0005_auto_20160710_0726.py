# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0004_auto_20160710_0722'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='height',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='page',
            name='width',
            field=models.SmallIntegerField(default=0),
        ),
    ]
