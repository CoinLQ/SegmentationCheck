# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0007_remove_sutra_normal_sutra'),
    ]

    operations = [
        migrations.AddField(
            model_name='sutra',
            name='normal_sutra',
            field=models.ForeignKey(default='', to='catalogue.NormalizeSutra'),
            preserve_default=False,
        ),
    ]
