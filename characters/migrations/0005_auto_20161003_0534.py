# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0004_usercredit_active_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercredit',
            name='active_date',
            field=models.CharField(max_length=8, null=True, blank=True),
        ),
    ]
