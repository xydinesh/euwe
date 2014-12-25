from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import transaction

from pyramid import testing
from .models import DBSession

class TestMyViewSuccessCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            MyModel,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = MyModel(name='one', value=55)
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_passing_view(self):
        from .views import EuweViews
        request = testing.DummyRequest()
        inst = EuweViews(request)
        info = inst.my_view()
        self.assertEqual(info['one'].name, 'one')
        self.assertEqual(info['project'], 'euwe')

class EuweUnitTestViews(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        # this tests throw an exception
        # found answer here
        # https://github.com/Pylons/pyramid/issues/1202
        self.config.add_route('login', '/login')

    def tearDown(self):
        testing.tearDown()

    def test_login_view(self):
        from .views import EuweViews
        request = testing.DummyRequest()
        inst = EuweViews(request)
        info = inst.login_view()
        self.assertEqual('Euwe Login Page', info['title'])

class EuweFunctionalTests(unittest.TestCase):
    def setUp(self):
        from pyramid.paster import get_app
        app = get_app('development.ini')
        from webtest import TestApp
        self.testapp = TestApp(app)
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home_url(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'Euwe' in res.body)

    def test_login_url(self):
        res = self.testapp.get('/login', status=200)
        self.assertIn(b'Euwe Login Page', res.body)
        self.assertIn(b'username', res.body)
        self.assertIn(b'password', res.body)

    def test_username_password(self):
        res = self.testapp.get('/login', status=200)
        form = res.form
        form['username'] = 'max'
        form['password'] = 'user_max'
        res = form.submit('form.submitted')
        self.assertEqual(res.status_int, 302)

    def test_invalid_username_password(self):
        res = self.testapp.get('/login', status=200)
        form = res.form
        form['username'] = 'max'
        form['password'] = 'max123'
        res = form.submit('form.submitted')
        self.assertIn(b'Invalid Login, Try again', res.body)



class EuweBlackBoxTests(unittest.TestCase):
    # user max logs in by putting his username and password
    # when he logs in he gets tactics to work on
    # he tries and solve the problem
    # then he gets the next problem
    # he use the hint button
    # he still can not do this, decide to try later
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

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


    def test_username_password(self):
        self.browser.get('http://localhost:6543')
        login_url = self.browser.current_url
