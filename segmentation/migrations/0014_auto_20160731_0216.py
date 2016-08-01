# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0013_page_image2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='image2',
        ),
        migrations.AlterField(
            model_name='page',
            name='image',
            field=models.ImageField(max_length=512, null=True, upload_to=b'page_images'),
        ),
    ]
