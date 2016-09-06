# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_auto_20160824_2255'),
        ('managerawdata', '0007_auto_20160905_1325'),
        ('segmentation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='verification_user_id',
        ),
        migrations.RemoveField(
            model_name='page',
            name='image2',
        ),
        migrations.AddField(
            model_name='character',
            name='region_no',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='page',
            name='o_page',
            field=models.ForeignKey(related_name='pages', blank=True, to='managerawdata.OPage', null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='volume',
            field=models.ForeignKey(related_name='pages', blank=True, to='catalogue.Volume', null=True),
        ),
        migrations.AlterField(
            model_name='characterstatistics',
            name='err_cnt',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='characterstatistics',
            name='total_cnt',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='characterstatistics',
            name='uncertainty_cnt',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='characterstatistics',
            name='uncheck_cnt',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='page',
            name='erro_char_cnt',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='page',
            name='height',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='page',
            name='is_correct',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='page',
            name='left',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='page',
            name='right',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='page',
            name='width',
            field=models.SmallIntegerField(default=0),
        ),
    ]
