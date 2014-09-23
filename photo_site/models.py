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
                                           options={'quality': 60})
    thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFill(300, 300)],
                                      format='JPEG',
                                      options={'quality': 60})

    
    def __unicode__(self):
        return '{0}'.format(self.title)


"""
In [49]: user = User.objects.get(username='eric')

In [50]: user.email
Out[50]: u'eric@eric.com'

In [60]: user.images_set.create(file_name='Testing', title='Test!', description='Party time!')
Out[60]: <Images: Test!>

# filter returns a queryset
# queryset must be iterated over for contents
In [17]: user = User.objects.filter(email='eric@eric.com')
In [19]: for item in user:
   ....:     print item.id
   ....:     
2

# user get and user__username (or email) to query across relationships
# user var does not need to be defined first
# in this case, user is the model name
In [31]: image = Images.objects.get(user__username='eric')
In [33]: image.id
Out[33]: 1

In [34]: image.title
Out[34]: u'Vacation'

In [8]: image = Images.objects.get(user__email='john@john.com')

In [9]: image.title
Out[9]: u'Test!'

# setting images based on user
In [16]: p = User.objects.get(username='eric')
In [25]: p.images_set.create(file_url="https://s3.amazonaws.com/photosite-django/users/eric/photos/Arsenal_2.jpg", title='Arsenal!', description='Arsenal crest')
Out[25]: <Images: Arsenal!>
In [26]: p.save()


# for multiple objects use below via filter
In [9]: user = Images.objects.filter(user__email='eric@eric.com')

In [10]: for items in user:
   ....:     print items.file_url
   ....:     
https://s3.amazonaws.com/photosite-django/users/eric/photos/Arsenal_2.jpg
http://www.google.com

# check if url exists
# would be unique for each user, so this works
In [18]: Images.objects.filter(file_url='https://s3.amazonaws.com/photosite-django/users/eric/photos/Arsenal_2.jpg').exists()
Out[18]: True


# creates group and save group name
In [2]: group = Group(name = 'Premium')
In [3]: group.save()

# check and call group name
In [4]: group = Group.objects.get(name = 'Premium')
In [5]: group
Out[5]: <Group: Premium>

# check if user in a group
users = group.user_set.all()

# add user to group
user = User.objects.get(username='eric')

In [10]: user.groups.add(group)

In [11]: user.groups.all()
Out[11]: [<Group: Premium>]

# check if user is in the group
In [21]: user.groups.filter(name = 'Premium').exists()
Out[21]: True

"""