from django.db import models
from django.contrib.auth.models import User


class UserCredit(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    username = models.CharField(max_length=32, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    credit = models.IntegerField(default=0)
    def __str__(self):
        return "%s's credit:%d" % self.user,self.credit
