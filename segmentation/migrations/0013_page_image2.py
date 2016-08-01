# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0012_auto_20160728_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='image2',
            field=models.ImageField(max_length=512, null=True, upload_to=b'page_images'),
        ),
    ]
