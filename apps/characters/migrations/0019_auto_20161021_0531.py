# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0018_auto_20161020_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='charstock',
            name='l_value',
            field=models.DecimalField(default=0, max_digits=4, decimal_places=3),
        ),
        migrations.AddField(
            model_name='charstock',
            name='r_value',
            field=models.DecimalField(default=0, max_digits=4, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='charstock',
            name='character',
            field=models.OneToOneField(primary_key=True, serialize=False, to='segmentation.CharacterStatistics'),
        ),
    ]
