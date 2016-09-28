from django.db import models
from django.contrib.auth.models import User
from segmentation.models import Character
from datetime import datetime

# Create your models here.
class QuizResult(models.Model):
    user = models.ForeignKey(User)
    character = models.ForeignKey(Character)
    is_correct = models.SmallIntegerField()
    right_wrong = models.BooleanField()
    batch = models.ForeignKey(QuizBatch)

class QuizBatch(models.Model):
    user = models.ForeignKey(User)
    score = models.FloatField(default=0.0)
    time = models.DateTimeField(default=datetime.now())

