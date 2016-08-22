# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0011_page_erro_char_cnt'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='left',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='page',
            name='right',
            field=models.SmallIntegerField(default=0),
        ),
    ]
