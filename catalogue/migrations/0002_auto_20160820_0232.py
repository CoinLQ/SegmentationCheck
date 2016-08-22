# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripitaka',
            name='product_date',
            field=models.DateField(verbose_name='Tripitaka|product_date'),
        ),
    ]
