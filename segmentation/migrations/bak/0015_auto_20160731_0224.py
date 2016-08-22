# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0014_auto_20160731_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='image',
            field=models.ImageField(max_length=512, null=True, upload_to=b'character_images'),
        ),
    ]
