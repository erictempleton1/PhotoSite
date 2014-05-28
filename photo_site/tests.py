from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase, Client, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from photo_site.models import Images
from photo_site.forms import SignupForm, LoginForm, UploadFileForm, ChangePWForm
from photo_site.views import change_pw, user_page, login_user

class TestingImage(LiveServerTestCase):
    # creates json versions of db's to test against
    fixtures = ['photo_site_views_testdata.json', 'user_model.json']
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        #self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    """
    def test_create_account(self):
        self.browser.get(self.live_server_url + '/main/signup/')

        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('eric67')

        email_field = self.browser.find_element_by_name('email')
        email_field.send_keys('eric67@eric.com')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('eric')

        password_again_field = self.browser.find_element_by_name('password_again')
        password_again_field.send_keys('eric')

        password_again_field.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Login', body.text)
    

    def test_reset_pw(self):
        self.browser.get(self.live_server_url + '/main/login')

        # login using below credentials
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('eric')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('eric')
        password_field.send_keys(Keys.RETURN)

        # clicks on user admin link
        admin_link = self.browser.find_elements_by_link_text('Change Password')
        admin_link[0].click()

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Update', body.text)
    """

    def test_change_email(self):
        self.browser.get(self.live_server_url + '/main/login')

        # login using below credentials
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('eric')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('eric')
        password_field.send_keys(Keys.RETURN)

        email_link = self.browser.find_elements_by_link_text('Change Email')
        email_link[0].click()

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Change', body.text)








        
