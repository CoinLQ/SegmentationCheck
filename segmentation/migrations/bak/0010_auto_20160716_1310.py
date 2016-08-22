# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0009_auto_20160716_0255'),
    ]

    operations = [
        migrations.RenameField(
            model_name='characterstatistics',
            old_name='checked_cnt',
            new_name='err_cnt',
        ),
    ]
