# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managerawdata', '0002_auto_20160820_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opage',
            name='height',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='opage',
            name='image',
            field=models.ImageField(max_length=512, null=True, upload_to=b'opage_images', blank=True),
        ),
        migrations.AlterField(
            model_name='opage',
            name='pages_no',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='opage',
            name='width',
            field=models.SmallIntegerField(default=0),
        ),
    ]
