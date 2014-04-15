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

    

"""
In [49]: user = User.objects.get(username='eric')

In [50]: user.email
Out[50]: u'eric@eric.com'

In [60]: user.images_set.create(file_name='Testing', title='Test!', description='Party time!')
Out[60]: <Images: Test!>

"""