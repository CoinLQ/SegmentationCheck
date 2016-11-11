# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0012_character_line_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='line_no',
        ),
    ]
