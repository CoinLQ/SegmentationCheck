# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0003_usercredit_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercredit',
            name='active_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
