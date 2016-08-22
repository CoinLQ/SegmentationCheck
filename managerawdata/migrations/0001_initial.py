# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('credit', models.CharField(max_length=64)),
                ('admin_description', models.CharField(max_length=64)),
                ('creator', models.CharField(max_length=64)),
                ('tag', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('alt', models.CharField(max_length=64)),
                ('caption', models.CharField(max_length=64)),
            ],
        ),
    ]
