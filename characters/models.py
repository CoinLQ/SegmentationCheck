# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from segmentation.models import Character
from django.db import transaction
from django.utils import timezone
from django.db.models import Q
from classification_statistics.models import DataPoint
from django.db.models.signals import post_save
from segmentation.models import CharacterStatistics
import time

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
    auto_apply = models.BooleanField(u'是否自动更新', default=False)

    class Meta:
        permissions = (
            ("update_result", "更新分类结果到字表"),
        )

    @classmethod
    def create(cls, char, algorithm, train_count, predict_count, started, completed, fetch_spent, training_spent, predict_spent, auto_apply):
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
        obj.auto_apply = auto_apply
        return obj

    def update_result(self):
        if self.updated:
            return
        with transaction.atomic():
            for result in ClassificationCompareResult.objects.filter(task_id=self.id):
                Character.objects.filter(id=result.character_id).update(accuracy=result.new_accuracy)
            CharStock.objects.get(pk=self.char).calc_accuracy_stat()
            self.updated = True
            self.save()


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

class CharStock(models.Model):
    character = models.OneToOneField(CharacterStatistics, to_field='char', primary_key=True)
    total_num = models.SmallIntegerField(u'总数', default=0)
    spent = models.IntegerField(u'总时间(秒)',blank=True, null=True)
    weight = models.DecimalField(default=0, max_digits=4, decimal_places=3, db_index= True)
    l_value = models.DecimalField(default=0, max_digits=4, decimal_places=3)
    r_value = models.DecimalField(default=0, max_digits=4, decimal_places=3)

    @transaction.atomic
    def calc_accuracy_stat(self):
        start_time = time.time()
        characters = Character.objects.filter(char=self.pk).filter(~Q(accuracy=-1))
        DataPoint.objects.filter(char=self.pk).delete()
        stat_points = [0] * 1001
        data_points = []
        for ch in characters:
            idx = ch.accuracy
            if idx < 0:
                continue
            stat_points[idx] += 1

        for idx in range(1001):
            dp = DataPoint(char=self.pk, range_idx=idx, count=stat_points[idx])
            data_points.append(dp)

        DataPoint.objects.bulk_create(data_points)
        self.spent = int(time.time() - start_time)
        self.weight = self.acc_weight(data_points)
        self.save()

    @classmethod
    @transaction.atomic
    def rebuild_table(cls):
        CharStock.objects.all().delete()
        for char_dict in Character.objects.values('char').distinct():
            ch = CharStock(character=char_dict['char'])
            ch.save()

    def acc_weight(self, bp_query = None):
        bp_query = bp_query or DataPoint.objects.filter(char=self.pk)
        base = 500 # 1001 / 2
        front, end, l_count, r_count = 0, 0, 0, 0
        for dp in bp_query:
            if dp.range_idx >= base:
                r_count += dp.count
                end += dp.range_idx  * dp.count
            else:
                l_count += dp.count
                front +=  dp.range_idx * dp.count

        if r_count*l_count != 0:
            res = (end/r_count - front/l_count)*1.0/1000
            self.l_value = (front/l_count)*1.0/1000
            self.r_value = (end/r_count)*1.0/1000
        else:
            res = 0

        return res


class CharCutRecord(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    character = models.ForeignKey(Character)
    is_correct = models.SmallIntegerField()
    img_filename = models.CharField(max_length=512)
    left = models.SmallIntegerField()
    right = models.SmallIntegerField()
    top = models.SmallIntegerField()
    bottom = models.SmallIntegerField()
    line_no = models.SmallIntegerField()
    char_no = models.SmallIntegerField()
    region_no = models.SmallIntegerField(default=0)
    time = models.DateTimeField()
    direct = models.CharField(max_length=7)
    degree = models.SmallIntegerField()

    @classmethod
    def create(cls, user, ch, file_path, direct, degree):
        obj = cls()
        obj.user = user
        obj.character_id = ch.pk
        obj.is_correct = ch.is_correct
        obj.left = ch.left
        obj.right = ch.right
        obj.top = ch.top
        obj.bottom = ch.bottom
        obj.line_no = ch.line_no
        obj.char_no = ch.char_no
        obj.region_no = ch.region_no
        obj.time = timezone.now()
        obj.img_filename = file_path
        obj.direct = direct
        obj.degree = degree
        return obj

    def __unicode__(self):
        return u'时间%s: %s 被 %s 往 %s 方向切分 %s 像素' % (self.time, self.character_id, self.user, self.direct, self.degree )

