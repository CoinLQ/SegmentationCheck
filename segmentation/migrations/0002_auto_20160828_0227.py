# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_auto_20160824_2255'),
        ('segmentation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opage',
            name='sutra_info',
        ),
        migrations.RemoveField(
            model_name='opage',
            name='tripitaka',
        ),
        migrations.RemoveField(
            model_name='opage',
            name='volume',
        ),
        migrations.RemoveField(
            model_name='sutrainfo',
            name='sutra',
        ),
        migrations.RemoveField(
            model_name='sutrainfo',
            name='tripitaka',
        ),
        migrations.RemoveField(
            model_name='volume',
            name='tripitaka',
        ),
        migrations.AddField(
            model_name='page',
            name='volume',
            field=models.ForeignKey(related_name='pages', default=0, to='catalogue.Volume'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='o_page',
            field=models.ForeignKey(blank=True, to='managerawdata.OPage', null=True),
        ),
        migrations.DeleteModel(
            name='OPage',
        ),
        migrations.DeleteModel(
            name='Sutra',
        ),
        migrations.DeleteModel(
            name='SutraInfo',
        ),
        migrations.DeleteModel(
            name='Tripitaka',
        ),
        migrations.DeleteModel(
            name='Volume',
        ),
    ]
