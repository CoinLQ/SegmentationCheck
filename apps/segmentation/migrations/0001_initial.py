# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('char', models.CharField(max_length=4, db_index=True)),
                ('image', models.CharField(max_length=512)),
                ('left', models.SmallIntegerField()),
                ('right', models.SmallIntegerField()),
                ('top', models.SmallIntegerField()),
                ('bottom', models.SmallIntegerField()),
                ('line_no', models.SmallIntegerField()),
                ('char_no', models.SmallIntegerField()),
                ('verification_user_id', models.IntegerField(blank=True,null=True)),
                ('is_correct', models.SmallIntegerField(default=0, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='CharacterStatistics',
            fields=[
                ('char', models.CharField(max_length=4, serialize=False, primary_key=True, db_index=True)),
                ('total_cnt', models.IntegerField()),
                ('uncheck_cnt', models.IntegerField()),
                ('err_cnt', models.IntegerField()),
                ('uncertainty_cnt', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('image', models.CharField(max_length=512)),
                ('text', models.TextField()),
                ('height', models.SmallIntegerField()),
                ('width', models.SmallIntegerField()),
                ('is_correct', models.SmallIntegerField()),
                ('erro_char_cnt', models.IntegerField()),
                ('left', models.SmallIntegerField()),
                ('right', models.SmallIntegerField()),
                ('image2', models.CharField(max_length=512,null=True,blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='page',
            field=models.ForeignKey(to='segmentation.Page'),
        ),
    ]
