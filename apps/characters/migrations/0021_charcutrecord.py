# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0009_character_is_integrity'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('characters', '0020_classificationtask_auto_apply'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharCutRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_correct', models.SmallIntegerField()),
                ('img_filename', models.CharField(max_length=512)),
                ('left', models.SmallIntegerField()),
                ('right', models.SmallIntegerField()),
                ('top', models.SmallIntegerField()),
                ('bottom', models.SmallIntegerField()),
                ('line_no', models.SmallIntegerField()),
                ('char_no', models.SmallIntegerField()),
                ('region_no', models.SmallIntegerField(default=0)),
                ('time', models.DateTimeField()),
                ('direct', models.CharField(max_length=5)),
                ('degree', models.SmallIntegerField()),
                ('character', models.ForeignKey(to='segmentation.Character')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
