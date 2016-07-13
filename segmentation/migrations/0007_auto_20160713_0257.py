# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0006_characterstatistics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='characterstatistics',
            name='checked_cnt',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='characterstatistics',
            name='total_cnt',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='characterstatistics',
            name='uncertainty_cnt',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='characterstatistics',
            name='uncheck_cnt',
            field=models.IntegerField(default=0),
        ),
    ]
