# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0016_auto_20161115_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='is_same',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='character',
            name='recog_chars',
            field=django.contrib.postgres.fields.ArrayField(default=[], base_field=models.CharField(max_length=4, blank=True), size=10),
        ),
        migrations.AlterIndexTogether(
            name='character',
            index_together=set([('char', 'is_correct'), ('char', 'is_same'), ('char', 'accuracy')]),
        ),
    ]
