from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from random import randint
import datetime
import os, traceback

class Images(models.Model):

    # creates s3 bucket with username, and appends user id to file.
    def photo_location(instance, filename):
        split_filename = filename.split('.')
        filename_lower = '%s.%s' % (split_filename[0], split_filename[-1].lower())
        filename = '%s_%s' % (instance.user.id, filename_lower)
        return '/'.join([instance.user.username, 'images', filename])
        
    # also created seperate bucket for thumbs with same format.
    def thumb_location(instance, filename):
        split_filename = filename.split('.')
        filename_lower = '%s.%s' % (split_filename[0], split_filename[-1].lower())
        filename = '%s_%s' % (instance.user.id, filename_lower)
        return '/'.join([instance.user.username, 'thumbnails', filename])

    user = models.ForeignKey(User)
    orig_filename = models.CharField(max_length=300)
    filename = models.CharField(max_length=300)
    file_url = models.CharField(max_length=300)
    thumb_url = models.CharField(max_length=300)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=photo_location)
    thumbnail = models.ImageField(upload_to=thumb_location)

    
    def __unicode__(self):
        return '%s' % self.title

    def create_thumbnail(self):

        if not self.image:
            return

        from PIL import Image
        from cStringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        thumb_size = (300, 300)

        DJANGO_TYPE = self.image.file.content_type
 
        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'

        # open original image
        image = Image.open(StringIO(self.image.read()))

        # prevent distortion using antialias
        image.thumbnail(thumb_size, Image.ANTIALIAS)

        # save thumbnail
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # user django suf to save image
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                  temp_handle.read(), content_type=DJANGO_TYPE)

        self.thumbnail.save('thumb_%s.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)

    def save(self, *args, **kwargs):
        # create thumb
        self.create_thumbnail()
        super(Images, self).save(*args, **kwargs)
    
    

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


# creates group
In [2]: group = Group(name = 'Premium')

In [3]: group.save()

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
"""