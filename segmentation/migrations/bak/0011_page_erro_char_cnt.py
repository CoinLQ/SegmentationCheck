# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0010_auto_20160716_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='erro_char_cnt',
            field=models.IntegerField(default=0),
        ),
    ]
