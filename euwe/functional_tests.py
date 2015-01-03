from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import transaction
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid import testing
from .models import DBSession
from unittest.mock import patch

class EuweBlackBoxTests(unittest.TestCase):
    # user max logs in by putting his username and password
    # when he logs in he gets tactics to work on
    # he tries and solve the problem
    # then he gets the next problem
    # he use the hint button
    # he still can not do this, decide to try later
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_browser_title(self):
        self.browser.get('http://localhost:6543')
        self.assertIn('Euwe', self.browser.title)

    def test_login_page(self):
        self.browser.get('http://localhost:6543/login')

        self.assertIn('Euwe', self.browser.title)

        form = self.browser.find_element_by_tag_name('form')
        self.assertIn('/login', form.get_attribute('action'))

        inputbox = self.browser.find_element_by_id('id_username')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'username')

        password = self.browser.find_element_by_id('id_password')
        self.assertEqual(password.get_attribute('placeholder'), 'password')

        submit = self.browser.find_element_by_name('form.submitted')
        inputbox.send_keys('max')
        password.send_keys('max123')
        submit.submit()

    def test_fen_page(self):
        self.browser.get('http://localhost:6543/fen?id=1')
        self.assertIn('Euwe', self.browser.title)
        self.assertIn('r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R',
        self.browser.page_source)
        self.browser.quit()

        self.browser = webdriver.Firefox()
        self.browser.get('http://localhost:6543/fen?id=100')
        self.assertNotIn('r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R',
        self.browser.page_source)

    def test_edit_page(self):
        self.browser.get('http://localhost:6543/edit')
        self.assertIn('Euwe', self.browser.title)

        btn_start = self.browser.find_element_by_id('id_btn_start')
        self.assertEqual(btn_start.get_attribute('value'), 'Start Position')

        btn_clear = self.browser.find_element_by_id('id_btn_clear')
        self.assertEqual(btn_clear.get_attribute('value'), 'Clear')

        btn_save = self.browser.find_element_by_id('id_btn_save')
        self.assertEqual(btn_save.get_attribute('value'), 'Save')

        text_area = self.browser.find_element_by_id('id_text_area')
        self.assertEqual(text_area.get_attribute('col'), '100')
        self.assertEqual(text_area.get_attribute('height'), '20')

        self.fail('Finish position edit !')
