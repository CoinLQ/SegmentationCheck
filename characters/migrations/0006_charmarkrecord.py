# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0005_auto_20161002_1615'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('characters', '0005_auto_20161003_0534'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharMarkRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_correct', models.SmallIntegerField()),
                ('time', models.DateTimeField()),
                ('character', models.ForeignKey(to='segmentation.Character')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
