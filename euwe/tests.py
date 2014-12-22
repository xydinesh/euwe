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
        from .views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['one'].name, 'one')
        self.assertEqual(info['project'], 'euwe')


class TestMyViewFailureCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            MyModel,
            )
        DBSession.configure(bind=engine)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_failing_view(self):
        from .views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info.status_int, 500)

class EuweFunctionalTests(unittest.TestCase):
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

    def test_username_password(self):
        self.browser.get('http://localhost:6543')
        inputbox = self.browser.find_element_by_id('id_username')
        self.assertEqual(inputbox.get_atrribute('placeholder'), 'username')

        password = self.browser.find_element_by_id('id_password')
        self.assertEqual(password.get_atrribute('placeholder'), '')

        submit = self.browser.find_elmement_by_name('submit')

        inputbox.send_keys('max')
        inputbox.send_keys(Keys.ENTER)

        password.send_keys('max123')
        password.send_keys(Keys.ENTER)

        submit.submit()
