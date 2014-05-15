from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase, Client

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from photo_site.models import Images
from photo_site.forms import SignupForm, LoginForm, UploadFileForm, ChangePWForm
from photo_site.views import change_pw, user_page, login_user

class TestingImage(TestCase):
    # creates json versions of db's to test against
    fixtures = ['photo_site_views_testdata.json', 'user_model.json']
    
    def test_user_add(self):
        test_user1 = User.objects.create_user(username='eric', email='eric@eric.com', password='eric')
        self.assertTrue(isinstance(test_user1, User))
        self.assertEqual(test_user1.__unicode__(), test_user1.username)

    def test_view(self):
        response = self.client.get('/main/eric/photos/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user_images' in response.context)
