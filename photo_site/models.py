from django.db import models
from django.utils import timezone
import datetime

class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=15)

    def __unicode__(self):
        return '%s' % self.username

class Images(models.Model):
    user = models.ForeignKey(User)
    file_name = models.CharField(max_length=140)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=140)
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.title

    