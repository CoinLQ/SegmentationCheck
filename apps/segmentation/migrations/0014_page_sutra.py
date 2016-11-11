# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_auto_20161111_0947'),
        ('segmentation', '0013_remove_character_line_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='sutra',
            field=models.ForeignKey(related_name='pages', blank=True, to='catalogue.Sutra', null=True),
        ),
    ]
