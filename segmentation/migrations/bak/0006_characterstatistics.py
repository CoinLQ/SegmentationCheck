# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0005_auto_20160710_0726'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterStatistics',
            fields=[
                ('char', models.CharField(max_length=4, serialize=False, primary_key=True, db_index=True)),
                ('total_cnt', models.IntegerField()),
                ('uncheck_cnt', models.IntegerField()),
                ('checked_cnt', models.IntegerField()),
                ('uncertainty_cnt', models.IntegerField()),
            ],
        ),
    ]
