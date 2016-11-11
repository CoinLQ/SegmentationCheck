# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_auto_20160824_2255'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(default=b'', max_length=12)),
                ('pages_count', models.SmallIntegerField(default=0, verbose_name='Reel|pages_count')),
                ('sutras', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.CharField(max_length=134), blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='normalizesutra',
            name='author',
        ),
        migrations.RemoveField(
            model_name='sutra',
            name='author',
        ),
        migrations.RemoveField(
            model_name='sutra',
            name='end',
        ),
        migrations.RemoveField(
            model_name='sutra',
            name='start',
        ),
        migrations.RemoveField(
            model_name='tripitaka',
            name='bars_count',
        ),
        migrations.RemoveField(
            model_name='volume',
            name='number',
        ),
        migrations.RemoveField(
            model_name='volume',
            name='pages_count',
        ),
        migrations.AddField(
            model_name='normalizesutra',
            name='era',
            field=models.CharField(default=b'', max_length=12),
        ),
        migrations.AddField(
            model_name='normalizesutra',
            name='sn',
            field=models.CharField(default=b'', max_length=12),
        ),
        migrations.AddField(
            model_name='sutra',
            name='end_page',
            field=models.SmallIntegerField(default=0, verbose_name='Sutra|end_page'),
        ),
        migrations.AddField(
            model_name='sutra',
            name='era',
            field=models.CharField(default=b'', max_length=12),
        ),
        migrations.AddField(
            model_name='sutra',
            name='reel_nm',
            field=models.SmallIntegerField(default=0, verbose_name='reel_nm'),
        ),
        migrations.AddField(
            model_name='sutra',
            name='sn',
            field=models.CharField(default=b'', max_length=12),
        ),
        migrations.AddField(
            model_name='sutra',
            name='start_page',
            field=models.SmallIntegerField(default=1, verbose_name='Sutra|start_page'),
        ),
        migrations.AddField(
            model_name='sutra',
            name='translator',
            field=models.CharField(default=b'', max_length=64),
        ),
        migrations.AddField(
            model_name='tripitaka',
            name='reel_nm',
            field=models.SmallIntegerField(default=0, verbose_name='Tripitaka|reel_nm'),
        ),
        migrations.AddField(
            model_name='volume',
            name='pages_nm',
            field=models.SmallIntegerField(default=0, verbose_name='Volume|pages_nm'),
        ),
        migrations.AddField(
            model_name='volume',
            name='sn',
            field=models.CharField(default=b'', max_length=12, verbose_name='Volume|sn'),
        ),
        migrations.AddField(
            model_name='volume',
            name='sutras',
            field=django.contrib.postgres.fields.ArrayField(default=[], size=None, base_field=models.CharField(max_length=134), blank=True),
        ),
        migrations.AlterField(
            model_name='normalizesutra',
            name='discription',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='normalizesutra',
            name='name',
            field=models.CharField(default=b'', max_length=128),
        ),
        migrations.AlterField(
            model_name='sutra',
            name='discription',
            field=models.CharField(default=b'', max_length=512),
        ),
        migrations.AlterField(
            model_name='sutra',
            name='name',
            field=models.CharField(default=b'', max_length=128),
        ),
        migrations.AlterField(
            model_name='tripitaka',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Tripitaka|name'),
        ),
        migrations.AlterField(
            model_name='tripitaka',
            name='product',
            field=models.CharField(max_length=64, verbose_name='Tripitaka|product'),
        ),
        migrations.AlterField(
            model_name='volume',
            name='start_page',
            field=models.SmallIntegerField(default=1, verbose_name='Volume|start_page'),
        ),
        migrations.AddField(
            model_name='reel',
            name='tripitaka',
            field=models.ForeignKey(related_name='reels', verbose_name='tripitaka', to='catalogue.Tripitaka'),
        ),
    ]
