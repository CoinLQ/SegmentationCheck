# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('char', models.CharField(max_length=4, db_index=True)),
                ('range_idx', models.SmallIntegerField()),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]
