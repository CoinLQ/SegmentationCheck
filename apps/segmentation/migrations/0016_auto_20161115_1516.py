# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0015_character_is_dirty'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='erro_char_cnt',
            new_name='accuracy',
        ),
    ]
