# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0004_auto_20161001_0921'),
    ]

    operations = [
        migrations.RenameField(
            model_name='characterstatistics',
            old_name='uncertainty_cnt',
            new_name='correct_cnt',
        ),
    ]
