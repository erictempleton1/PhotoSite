from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase

from django.contrib.auth.models import User
from photo_site.models import Images
from photo_site.forms import SignupForm, LoginForm, UploadFileForm, ChangePWForm
from photo_site.views import change_pw, user_page

class TestingImage(TestCase):

    def add_user(self):
        user = User.objects.create_user(username='eric', email='eric@eric.com', password='eric')
        return user

    def second_user(self):
        user = User.objects.create_user(username='eric1', email='eric@eric.com', password='eric')
        return user

    def test_user_add(self):
        w = self.add_user()
        q = self.second_user()
        self.assertTrue(isinstance(w, User))
        self.assertEqual(w.__unicode__(), w.username)

    def test_index(self):
        found = resolve('/main/1/photos/')
        self.assertEqual(found.func, user_page) 