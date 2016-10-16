# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0005_auto_20161002_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='accuracy',
            field=models.SmallIntegerField(default=-1, db_index=True),
        ),
    ]
