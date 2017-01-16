# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0017_auto_20170110_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='characterstatistics',
            name='recog_diff_count',
            field=models.IntegerField(default=0),
        ),
    ]
