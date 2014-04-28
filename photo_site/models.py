from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class Images(models.Model):
    user = models.ForeignKey(User, unique=True)
    image_file = models.FileField(upload_to='documents/%Y/%m/%d')
    title = models.CharField(max_length=100)
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.title

    

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


"""