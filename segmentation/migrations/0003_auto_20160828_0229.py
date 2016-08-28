# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0002_auto_20160828_0227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='volume',
            field=models.ForeignKey(related_name='pages', blank=True, to='catalogue.Volume', null=True),
        ),
    ]
