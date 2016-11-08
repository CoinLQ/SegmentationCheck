# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managerawdata', '0003_auto_20160822_0208'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='opage',
            options={'verbose_name': 'opage', 'verbose_name_plural': 'opages'},
        ),
        migrations.RenameField(
            model_name='opage',
            old_name='pages_no',
            new_name='page_no',
        ),
        migrations.AddField(
            model_name='opage',
            name='page_type',
            field=models.SmallIntegerField(default=1),
        ),
    ]
