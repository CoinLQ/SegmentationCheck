# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managerawdata', '0005_opage_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opage',
            name='volume',
            field=models.ForeignKey(related_name='o_pages', to='catalogue.Volume'),
        ),
    ]
