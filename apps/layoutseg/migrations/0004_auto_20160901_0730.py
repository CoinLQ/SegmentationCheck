# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layoutseg', '0003_auto_20160901_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='id',
            field=models.CharField(max_length=32, serialize=False, primary_key=True),
        ),
    ]
