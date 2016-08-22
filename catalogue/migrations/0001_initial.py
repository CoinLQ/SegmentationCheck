# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NormalizeSutra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('author', models.CharField(max_length=64)),
                ('discription', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Sutra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('author', models.CharField(max_length=64)),
                ('discription', models.CharField(max_length=512)),
                ('start', models.CharField(max_length=32)),
                ('end', models.CharField(max_length=32)),
                ('norma_sutra', models.ForeignKey(to='catalogue.NormalizeSutra')),
            ],
        ),
        migrations.CreateModel(
            name='Tripitaka',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Tripitaka|name')),
                ('code', models.CharField(max_length=10, verbose_name='Tripitaka|code')),
                ('product', models.CharField(max_length=128, verbose_name='Tripitaka|product')),
                ('product_date', models.DateTimeField(verbose_name='Tripitaka|product_date')),
                ('description', models.TextField(verbose_name='Tripitaka|description')),
                ('cover', models.ImageField(upload_to=b'cover', verbose_name='Tripitaka|cover')),
                ('volumes_count', models.SmallIntegerField(default=0, verbose_name='Tripitaka|volumes_count')),
                ('bars_count', models.SmallIntegerField(default=0, verbose_name='Tripitaka|bars_count')),
            ],
            options={
                'verbose_name': 'tripitaka',
                'verbose_name_plural': 'tripitakas',
            },
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.SmallIntegerField(verbose_name='Volume|number')),
                ('pages_count', models.SmallIntegerField(verbose_name='Volume|pages_count')),
                ('tripitaka', models.ForeignKey(verbose_name='Volume|tripitaka', to='catalogue.Tripitaka')),
            ],
            options={
                'verbose_name': 'Segmentation|volume',
                'verbose_name_plural': 'Segmentation|volumes',
            },
        ),
        migrations.AddField(
            model_name='sutra',
            name='tripitaka',
            field=models.ForeignKey(to='catalogue.Tripitaka'),
        ),
    ]
