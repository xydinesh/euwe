from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import transaction

from pyramid import testing
from .models import DBSession

def _initDB():
    from sqlalchemy import create_engine
    engine = create_engine('sqlite://')
    from .models import (
        Base,
        MyModel,
        PositionModel,
        )
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        model = MyModel(name='one', value=55)
        DBSession.add(model)

        position = PositionModel(category='position', fen='r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R')
        DBSession.add(position)
    return DBSession

class TestMyViewSuccessCondition(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.session = _initDB()

    def tearDown(self):
        self.session.remove()
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
        self.session = _initDB()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def test_login_view(self):
        # this tests throw an exception
        # found answer here
        # https://github.com/Pylons/pyramid/issues/1202
        self.config.add_route('login', '/login')
        from .views import EuweViews
        request = testing.DummyRequest()
        inst = EuweViews(request)
        info = inst.login_view()
        self.assertEqual('Euwe Login Page', info['title'])
        self.assertIn('Invalid Login, Try again', info['message'])

    def test_login_success_view(self):
        # this tests throw an exception
        # found answer here
        # https://github.com/Pylons/pyramid/issues/1202
        self.config.add_route('login', '/login')
        from .views import EuweViews
        request = testing.DummyRequest(params={'username': 'max', 'password': 'user_max', 'form.submitted': True})
        inst = EuweViews(request)
        info = inst.login_view()
        self.assertEqual(info.status_int, 302)

    def test_logout_view(self):
        # this tests throw an exception
        # found answer here
        # https://github.com/Pylons/pyramid/issues/1202
        self.config.add_route('home', '/')
        self.config.add_route('logout', '/logout')
        from .views import EuweViews
        request = testing.DummyRequest()
        inst = EuweViews(request)
        info = inst.logout_view()
        self.assertEqual(info.status_int, 302)

    def test_position_model(self):
        from .models import PositionModel
        pos = self.session.query(PositionModel).filter_by(id=1).first()
        self.assertTrue(pos.fen, b'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R')

    def test_fen_view(self):
        self.config.add_route('home', '/')
        self.config.add_route('fen', '/fen')
        from .views import EuweViews
        request = testing.DummyRequest(params={'id': 1})
        inst = EuweViews(request)
        info = inst.fen_view()
        pos = info['position']
        self.assertTrue(pos.fen, b'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R')

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

    def test_logout_url(self):
        res = self.testapp.get('/logout', status=302)
        self.assertEqual(res.status_int, 302)

    def test_fen_url(self):
        res = self.testapp.get('/fen', params={'id': 1}, status=200)
        self.assertIn(b'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R', res.body)

    def test_fen_url_invalid_id(self):
        res = self.testapp.get('/fen', params={'id': 150}, status=200)
        self.assertIn(b'start', res.body)



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
        self.browser.get('http://localhost:6543/positions/edit')
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
