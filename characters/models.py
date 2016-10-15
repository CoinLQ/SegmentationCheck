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
    char = models.CharField(max_length=4)
    algorithm = models.CharField(max_length=128)
    started = models.DateTimeField()
    completed = models.DateTimeField()
    spent = models.IntegerField()
    fetch_spent = models.IntegerField()
    training_spent = models.IntegerField()
    predict_spent = models.IntegerField()
    updated = models.BooleanField()

    @classmethod
    def create(cls, char, algorithm, started, completed, fetch_spent, training_spent, predict_spent):
        obj = cls()
        obj.char = char
        obj.algorithm = algorithm
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


