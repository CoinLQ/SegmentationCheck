# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_auto_20161111_0947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sutra',
            name='normal_sutra',
        ),
    ]
