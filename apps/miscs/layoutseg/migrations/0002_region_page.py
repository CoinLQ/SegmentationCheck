# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layoutseg', '0001_initial'),
        ('segmentation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='page',
            field=models.ForeignKey(default=1, to='segmentation.Page'),
            preserve_default=False,
        ),
    ]
