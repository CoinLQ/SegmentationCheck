# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0002_auto_20160906_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='accuracy',
            field=models.FloatField(default=-1.0),
        ),
    ]
