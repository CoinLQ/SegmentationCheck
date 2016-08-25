# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_auto_20160820_0232'),
    ]

    operations = [
        migrations.AddField(
            model_name='volume',
            name='end_page',
            field=models.SmallIntegerField(default=0, verbose_name='Volume|end_page'),
        ),
        migrations.AddField(
            model_name='volume',
            name='start_page',
            field=models.SmallIntegerField(default=0, verbose_name='Volume|start_page'),
        ),
        migrations.AlterField(
            model_name='volume',
            name='pages_count',
            field=models.SmallIntegerField(default=0, verbose_name='Volume|pages_count'),
        ),
        migrations.AlterField(
            model_name='volume',
            name='tripitaka',
            field=models.ForeignKey(related_name='volumes', verbose_name='Volume|tripitaka', to='catalogue.Tripitaka'),
        ),
    ]
