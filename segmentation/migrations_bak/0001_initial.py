# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_auto_20160824_2255'),
    ]

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
                ('is_correct', models.SmallIntegerField(default=0, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='CharacterStatistics',
            fields=[
                ('char', models.CharField(max_length=4, serialize=False, primary_key=True, db_index=True)),
                ('total_cnt', models.IntegerField(default=0)),
                ('uncheck_cnt', models.IntegerField(default=0)),
                ('err_cnt', models.IntegerField(default=0)),
                ('uncertainty_cnt', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('image', models.CharField(max_length=512)),
                ('image_upload', models.ImageField(max_length=512, null=True, upload_to=b'page_images')),
                ('text', models.TextField()),
                ('width', models.SmallIntegerField(default=0)),
                ('height', models.SmallIntegerField(default=0)),
                ('left', models.SmallIntegerField(default=0)),
                ('right', models.SmallIntegerField(default=0)),
                ('is_correct', models.SmallIntegerField(default=0)),
                ('erro_char_cnt', models.IntegerField(default=0)),
                ('volume', models.ForeignKey(related_name='pages', blank=True, to='catalogue.Volume', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display', models.CharField(max_length=16)),
                ('is_base', models.BooleanField(default=False)),
                ('semanteme', models.ForeignKey(related_name='Text', blank=True, to='segmentation.Text')),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='page',
            field=models.ForeignKey(to='segmentation.Page'),
        ),
        migrations.AddField(
            model_name='character',
            name='text',
            field=models.ForeignKey(blank=True, to='segmentation.Text', null=True),
        ),
    ]
