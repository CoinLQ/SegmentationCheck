# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0006_auto_20161016_0836'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='character',
            index_together=set([('char', 'is_correct')]),
        ),
    ]
