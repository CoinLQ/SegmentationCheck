# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0009_auto_20161015_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classificationtask',
            name='algorithm',
            field=models.CharField(max_length=128, verbose_name='\u5206\u7c7b\u7b97\u6cd5'),
        ),
        migrations.AlterField(
            model_name='classificationtask',
            name='char',
            field=models.CharField(max_length=4, verbose_name='\u5b57'),
        ),
        migrations.AlterField(
            model_name='classificationtask',
            name='completed',
            field=models.DateTimeField(verbose_name='\u5b8c\u6210\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='classificationtask',
            name='fetch_spent',
            field=models.IntegerField(verbose_name='\u53d6\u6570\u636e\u7528\u7684\u65f6\u95f4(\u79d2)'),
        ),
        migrations.AlterField(
            model_name='classificationtask',
            name='predict_count',
            field=models.IntegerField(default=0, verbose_name='\u9884\u6d4b\u6837\u672c\u6570'),
        ),
        migrations.AlterField(
            model_name='classificationtask',
            name='predict_spent',
            field=models.IntegerField(verbose_name='\u9884\u6d4b\u65f6\u95f4(\u79d2)'),
        ),
        migrations.AlterField(
            model_name='classificationtask',
            name='spent',
            field=models.IntegerField(verbose_name='\u603b\u65f6\u95f4(\u79d2)'),
        ),
        migrations.AlterField(
            model_name='classificationtask',
            name='started',
            field=models.DateTimeField(verbose_name='\u5f00\u59cb\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='classificationtask',
            name='train_count',
            field=models.IntegerField(default=0, verbose_name='\u8bad\u7ec3\u6837\u672c\u6570'),
        ),
        migrations.AlterField(
            model_name='classificationtask',
            name='training_spent',
            field=models.IntegerField(verbose_name='\u8bad\u7ec3\u65f6\u95f4(\u79d2)'),
        ),
        migrations.AlterField(
            model_name='classificationtask',
            name='updated',
            field=models.BooleanField(verbose_name='\u662f\u5426\u5df2\u66f4\u65b0\u7ed3\u679c'),
        ),
    ]
