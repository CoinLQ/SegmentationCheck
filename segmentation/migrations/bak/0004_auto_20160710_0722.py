# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0003_auto_20160623_0150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='is_correct',
            field=models.SmallIntegerField(default=0),
        ),
    ]
