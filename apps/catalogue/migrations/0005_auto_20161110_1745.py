# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_auto_20161110_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='normalizesutra',
            name='id',
        ),
        migrations.RemoveField(
            model_name='sutra',
            name='sn',
        ),
        migrations.AlterField(
            model_name='normalizesutra',
            name='name',
            field=models.CharField(default=b'', max_length=128, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='sutra',
            name='id',
            field=models.CharField(default=b'', max_length=12, serialize=False, primary_key=True),
        ),
    ]
