# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('segmentation', '0002_auto_20160906_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizBatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(default=0.0)),
                ('time', models.DateTimeField(default=datetime.datetime(2016, 9, 29, 10, 18, 6, 922269))),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_correct', models.SmallIntegerField()),
                ('right_wrong', models.BooleanField()),
                ('batch', models.ForeignKey(to='quiz.QuizBatch')),
                ('character', models.ForeignKey(to='segmentation.Character')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
