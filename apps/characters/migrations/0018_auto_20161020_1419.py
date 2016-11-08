# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0017_auto_20161020_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charstock',
            name='character',
            field=models.OneToOneField(primary_key=True, serialize=False, to='segmentation.CharacterStatistics',to_field='char',db_constraint=False),
        ),
    ]
