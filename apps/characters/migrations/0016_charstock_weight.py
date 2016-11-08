# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0015_charstock'),
    ]

    operations = [
        migrations.AddField(
            model_name='charstock',
            name='weight',
            field=models.DecimalField(default=0, max_digits=4, decimal_places=3, db_index=True),
        ),
    ]
