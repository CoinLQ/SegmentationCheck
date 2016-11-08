# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0010_auto_20161016_0836'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharStock',
            fields=[
                ('character', models.CharField(max_length=4, serialize=False, verbose_name='\u5b57', primary_key=True)),
                ('total_num', models.SmallIntegerField(default=0, verbose_name='\u603b\u6570')),
                ('spent', models.IntegerField(null=True, verbose_name='\u603b\u65f6\u95f4(\u79d2)', blank=True)),
            ],
        ),
    ]
