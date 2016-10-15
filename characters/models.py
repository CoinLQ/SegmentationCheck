# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from segmentation.models import Character
from datetime import datetime

class UserCredit(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    username = models.CharField(max_length=32, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    active_date = models.CharField(max_length=8, null=True, blank=True)
    credit = models.IntegerField(default=0)
    def __str__(self):
        return "%s's credit:%d" % self.user,self.credit

class CharMarkRecord(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    character = models.ForeignKey(Character)
    is_correct = models.SmallIntegerField()
    time = models.DateTimeField()

    @classmethod
    def create(cls, user, character_id, is_correct, time):
        obj = cls()
        obj.user = user
        obj.character_id = character_id
        obj.is_correct = is_correct
        obj.time = time
        return obj

    def __unicode__(self):
        return u'%s 修改 %s 为 %d, 时间%s' % (self.user, self.character_id, self.is_correct, self.time)

class ClassificationTask(models.Model):
    char = models.CharField(u'字', max_length=4)
    algorithm = models.CharField(u'分类算法', max_length=128)
    train_count = models.IntegerField(u'训练样本数', default=0)
    predict_count = models.IntegerField(u'预测样本数', default=0)
    started = models.DateTimeField(u'开始时间')
    completed = models.DateTimeField(u'完成时间')
    spent = models.IntegerField(u'总时间(秒)')
    fetch_spent = models.IntegerField(u'取数据用的时间(秒)')
    training_spent = models.IntegerField(u'训练时间(秒)')
    predict_spent = models.IntegerField(u'预测时间(秒)')
    updated = models.BooleanField(u'是否已更新结果')

    class Meta:
        permissions = (
            ("update_result", "更新分类结果到字表"),
        )

    @classmethod
    def create(cls, char, algorithm, train_count, predict_count, started, completed, fetch_spent, training_spent, predict_spent):
        obj = cls()
        obj.char = char
        obj.algorithm = algorithm
        obj.train_count = train_count
        obj.predict_count = predict_count
        obj.started = started
        obj.completed = completed
        obj.spent = (completed - started).seconds
        obj.fetch_spent = fetch_spent
        obj.training_spent = training_spent
        obj.predict_spent = predict_spent
        obj.updated = False
        return obj

class ClassificationCompareResult(models.Model):
    task = models.ForeignKey(ClassificationTask)
    character = models.ForeignKey(Character, db_index=False)
    origin_accuracy = models.SmallIntegerField()
    new_accuracy = models.SmallIntegerField()
    difference = models.SmallIntegerField()

    @classmethod
    def create(cls, task, character_id, origin_accuracy, new_accuracy):
        obj = cls()
        obj.task = task
        obj.character_id = character_id
        obj.origin_accuracy = origin_accuracy
        obj.new_accuracy = new_accuracy
        obj.difference = new_accuracy - origin_accuracy
        return obj


