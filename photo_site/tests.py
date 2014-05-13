from django.test import TestCase
from django.contrib.auth.models import User
from photo_site.models import Images
from photo_site.forms import SignupForm, LoginForm, UploadFileForm, ChangePWForm

class TestingImage(TestCase):

    def add_user(self, username='joey', email='joey@joey.com', password='joey'):
        return User.objects.create(username=username, email=email, password=password)

    """
    def add_image(self, file_url="testing", title="test", description="test!"):
        return Images.objects.create(file_url=file_url, title=title, description=description)
    """
    

    def test_user_add(self):
        w = self.add_user()
        self.assertTrue(isinstance(w, User))
        self.assertEqual(w.__unicode__(), w.username)
    