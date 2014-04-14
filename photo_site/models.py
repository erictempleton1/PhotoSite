from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class Images(models.Model):
    user = models.ForeignKey(User, unique=True)
    file_name = models.CharField(max_length=140)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=140)
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.title

    