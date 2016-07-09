from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Page(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    image = models.CharField(max_length=512)
    text = models.TextField()
    check_tag = models.SmallIntegerField(default=0)

    def __unicode__(self):
        return self.id

class Character(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    page = models.ForeignKey(Page)
    char = models.CharField(max_length=4, db_index=True)
    image = models.CharField(max_length=512)
    left = models.SmallIntegerField()
    right = models.SmallIntegerField()
    top = models.SmallIntegerField()
    bottom = models.SmallIntegerField()
    line_no = models.SmallIntegerField()
    char_no = models.SmallIntegerField()
    is_correct = models.SmallIntegerField(default=0)
    verification_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return u'%s:%s' % (self.id, self.char)

class CharacterSet(models.Model):
    id = models.AutoField(max_length=5,primary_key=True)
    char = models.CharField(max_length=4, db_index=True)
    count = models.IntegerField(default=0)
    check_tag = models.SmallIntegerField(default=0)

    def __unicode__(self):
        return u'%s:%s' % ( self.char,self.count)
