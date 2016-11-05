# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0009_character_is_integrity'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='character',
            index_together=set([('char', 'is_correct'), ('char', 'accuracy')]),
        ),
    ]
