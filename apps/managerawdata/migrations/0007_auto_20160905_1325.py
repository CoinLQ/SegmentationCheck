# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managerawdata', '0006_auto_20160828_0227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opage',
            name='image',
            field=models.CharField(max_length=512, null=True, blank=True),
        ),
    ]
