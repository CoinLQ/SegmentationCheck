# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0002_auto_20160905_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercredit',
            name='username',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
    ]
