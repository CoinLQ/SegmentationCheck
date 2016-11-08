# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0021_charcutrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charcutrecord',
            name='direct',
            field=models.CharField(max_length=7),
        ),
    ]
