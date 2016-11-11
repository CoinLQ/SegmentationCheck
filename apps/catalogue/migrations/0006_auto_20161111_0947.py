# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0005_auto_20161110_1745'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sutra',
            old_name='norma_sutra',
            new_name='normal_sutra',
        ),
        migrations.AlterField(
            model_name='sutra',
            name='end_page',
            field=models.CharField(default=b'', max_length=12, verbose_name='Sutra|end_page'),
        ),
        migrations.AlterField(
            model_name='sutra',
            name='start_page',
            field=models.CharField(default=b'', max_length=12, verbose_name='Sutra|start_page'),
        ),
    ]
