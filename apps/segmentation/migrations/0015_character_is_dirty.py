# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0014_page_sutra'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='is_dirty',
            field=models.BooleanField(default=False),
        ),
    ]
