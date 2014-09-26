from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase, Client, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from photo_site.models import Images
from photo_site.forms import SignupForm, LoginForm, UploadFileForm, ChangePWForm
from photo_site.views import change_pw, user_page, login_user

from django.conf import settings
import boto
from boto.s3.key import Key
from boto.s3.connection import Bucket, Key

class TestingImage(LiveServerTestCase):
    # creates json versions of db's to test against
    fixtures = ['images.json', 'users.json']
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        #self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def photo_login(self):
        self.browser.get(self.live_server_url + '/login/')

        email_field = self.browser.find_element_by_name('username')
        email_field.send_keys(settings.USERNAME)

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(settings.PASSWORD)

        password_field.send_keys(Keys.RETURN)

    """
    def test_login(self):
        self.photo_login()

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Upload', body.text)

    """

    def test_upload(self):
        self.photo_login()

        title_field = self.browser.find_element_by_name('title')
        title_field.send_keys('Testing')

        upload_file = self.browser.find_element_by_name('file')
        upload_file.click()








        
