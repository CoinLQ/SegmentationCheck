# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0019_auto_20161021_0531'),
    ]

    operations = [
        migrations.AddField(
            model_name='classificationtask',
            name='auto_apply',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u81ea\u52a8\u66f4\u65b0'),
        ),
    ]
