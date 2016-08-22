# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('char', models.CharField(max_length=4)),
                ('image', models.CharField(max_length=512)),
                ('left', models.SmallIntegerField()),
                ('right', models.SmallIntegerField()),
                ('top', models.SmallIntegerField()),
                ('bottom', models.SmallIntegerField()),
                ('line_no', models.SmallIntegerField()),
                ('char_no', models.SmallIntegerField()),
                ('is_correct', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('image', models.CharField(max_length=512)),
                ('text', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='page',
            field=models.ForeignKey(to='segmentation.Page'),
        ),
        migrations.AddField(
            model_name='character',
            name='verification_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
