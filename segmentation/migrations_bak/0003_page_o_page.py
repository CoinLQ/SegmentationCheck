# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managerawdata', '0006_auto_20160828_0227'),
        ('segmentation', '0002_character_region_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='o_page',
            field=models.ForeignKey(related_name='pages', blank=True, to='managerawdata.OPage', null=True),
        ),
    ]
