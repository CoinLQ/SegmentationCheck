# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0002_auto_20160617_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='char',
            field=models.CharField(max_length=4, db_index=True),
        ),
    ]
