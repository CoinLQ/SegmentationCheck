# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_auto_20160820_0232'),
        ('managerawdata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OPage',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('pages_no', models.SmallIntegerField()),
                ('image', models.ImageField(max_length=512, null=True, upload_to=b'opage_images')),
                ('width', models.SmallIntegerField()),
                ('height', models.SmallIntegerField()),
                ('tripitaka', models.ForeignKey(to='catalogue.Tripitaka')),
                ('volume', models.ForeignKey(to='catalogue.Volume')),
            ],
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
