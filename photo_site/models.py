from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, Transpose, ResizeToFit
import datetime
import os


class Images(models.Model):

    # creates s3 bucket with username, and appends user id to file.
    def photo_location(instance, filename):
        split_filename = filename.split('.')
        filename_lower = '{0}.{1}'.format(split_filename[0], split_filename[-1].lower())
        filename = '{0}_{1}'.format(instance.user.id, filename_lower)
        return '/'.join([instance.user.username, 'images', filename])

    user = models.ForeignKey(User)
    orig_filename = models.CharField(max_length=300)
    user_filename = models.CharField(max_length=300)
    title = models.CharField(max_length=100)
    added = models.DateTimeField(auto_now_add=True)
    image_url = models.CharField(max_length=300)
    thumbnail_url = models.CharField(max_length=300)
    image = ProcessedImageField(upload_to=photo_location,
                                           processors=[Transpose()],
                                           format='JPEG',
                                           options={'quality': 40})
    thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFill(300, 300)],
                                      format='JPEG',
                                      options={'quality': 40})

    
    def __unicode__(self):
        return '{0}'.format(self.title)