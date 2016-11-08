# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managerawdata', '0004_auto_20160826_0026'),
    ]

    operations = [
        migrations.AddField(
            model_name='opage',
            name='status',
            field=models.SmallIntegerField(default=0),
        ),
    ]
