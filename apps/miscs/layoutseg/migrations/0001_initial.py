# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=4, null=True, blank=True)),
                ('left', models.SmallIntegerField()),
                ('right', models.SmallIntegerField()),
                ('top', models.SmallIntegerField()),
                ('bottom', models.SmallIntegerField()),
                ('line_no', models.SmallIntegerField()),
                ('region_no', models.SmallIntegerField()),
                ('mark', models.CharField(max_length=2, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'region',
                'verbose_name_plural': 'regions',
            },
        ),
    ]
