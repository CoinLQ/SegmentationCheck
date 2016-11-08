# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0010_auto_20161105_2011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='line_no',
        ),
    ]
