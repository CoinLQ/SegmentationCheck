# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0005_auto_20161002_1615'),
        ('characters', '0006_charmarkrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassificationCompareResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('origin_accuracy', models.SmallIntegerField()),
                ('new_accuracy', models.SmallIntegerField()),
                ('difference', models.SmallIntegerField()),
                ('character', models.ForeignKey(to='segmentation.Character', db_index=False)),
            ],
        ),
        migrations.CreateModel(
            name='ClassificationTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('char', models.CharField(max_length=4)),
                ('algorithm', models.CharField(max_length=128)),
                ('started', models.DateTimeField()),
                ('completed', models.DateTimeField()),
                ('spent', models.IntegerField()),
                ('fetch_spent', models.IntegerField()),
                ('training_spent', models.IntegerField()),
                ('predict_spent', models.IntegerField()),
                ('updated', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='classificationcompareresult',
            name='task',
            field=models.ForeignKey(to='characters.ClassificationTask'),
        ),
    ]
