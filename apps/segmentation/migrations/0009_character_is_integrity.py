# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0008_characterstatistics_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='is_integrity',
            field=models.SmallIntegerField(default=0, db_index=True),
        ),
    ]
