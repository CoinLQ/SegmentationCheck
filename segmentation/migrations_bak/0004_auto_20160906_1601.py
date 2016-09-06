# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0003_page_o_page'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='text',
            name='semanteme',
        ),
        migrations.RemoveField(
            model_name='character',
            name='text',
        ),
        migrations.RemoveField(
            model_name='page',
            name='image_upload',
        ),
        migrations.DeleteModel(
            name='Text',
        ),
    ]
