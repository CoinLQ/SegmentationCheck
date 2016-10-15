# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0007_auto_20161015_1854'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classificationtask',
            options={'permissions': (('update_result', '\u66f4\u65b0\u5206\u7c7b\u7ed3\u679c\u5230\u5b57\u8868'),)},
        ),
    ]
