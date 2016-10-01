# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0003_character_accuracy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='accuracy',
            field=models.FloatField(default=-1.0, db_index=True),
        ),
    ]
