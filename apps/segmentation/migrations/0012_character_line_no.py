# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0011_remove_character_line_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='line_no',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
