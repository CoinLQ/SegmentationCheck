# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0008_auto_20161015_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='classificationtask',
            name='predict_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='classificationtask',
            name='train_count',
            field=models.IntegerField(default=0),
        ),
    ]
