from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import transaction
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid import testing
from .models import DBSession
from unittest.mock import patch

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

        position = PositionModel(category='position',
        userid='xydinesh@gmail.com',
        fen='r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R')
        DBSession.add(position)
    return DBSession

class DummyAuthenticationPolicy(object):
    def __init__(self, userid, extra_principals=()):
        self.userid = userid
        self.extra_principals = extra_principals

    def authenticated_userid(self, request):
        return self.userid

    def effective_principals(self, request):
        principals = [Everyone]
        if self.userid:
            principals += [Authenticated]
            principals += list(self.extra_principals)
        return principals

    def remember(self, request, userid, **kw):
        return []

    def forget(self, request):
        return []

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
        authn_policy = DummyAuthenticationPolicy(userid='xydinesh')
        authz_policy = ACLAuthorizationPolicy()
        self.config.set_authorization_policy(authz_policy)
        self.config.set_authentication_policy(authn_policy)
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
        request = testing.DummyRequest(params={'username': 'max',
        'password': 'user_max', 'form.submitted': True})
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

    def test_position_model_email(self):
        from .models import PositionModel
        pos = self.session.query(PositionModel).filter_by(userid='xydinesh@gmail.com').first()
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

    def test_edit_view(self):
        from .views import EuweViews
        request = testing.DummyRequest()
        inst = EuweViews(request)
        info = inst.edit_view()
        self.assertTrue('Edit' in info['title'])

    def test_save_view_fail(self):
        from .views import EuweViews
        from pyramid.httpexceptions import HTTPMethodNotAllowed
        request = testing.DummyRequest(params={'fen': 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R'})
        inst = EuweViews(request)
        res = inst.save_view()
        self.assertEqual(res.__class__, HTTPMethodNotAllowed)

    def test_perosna_login(self):
        from .views import EuweViews
        request = testing.DummyRequest()
        inst = EuweViews(request)
        info = inst.hello_world()
        self.assertIn(b'xydinesh', info.body)

    def test_list_view(self):
        from .views import EuweViews
        request = testing.DummyRequest()
        inst = EuweViews(request)
        res = inst.list_view()
        self.assertIn('List', res['title'])


class EuweFunctionalAuthTests(unittest.TestCase):
    def setUp(self):
        from pyramid.paster import get_app
        app = get_app('testing.ini')
        from webtest import TestApp
        self.testapp = TestApp(app)
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

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

    def test_forbidden_view(self):
        res = self.testapp.get('/', status=403)
        self.assertIn(b'Forbidden', res.body)

class EuweFunctionalTests(unittest.TestCase):
    
    def setUp(self):
        from pyramid.paster import get_app
        app = get_app('testing.ini')
        from webtest import TestApp
        self.testapp = TestApp(app)
        self.config = testing.setUp()
        res = self.testapp.get('/login', status=200)
        form = res.form
        form['username'] = 'max'
        form['password'] = 'user_max'
        res = form.submit('form.submitted')

    def tearDown(self):
        testing.tearDown()

    def test_home_url(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'Euwe' in res.body)

    def test_fen_url(self):
        res = self.testapp.get('/fen', params={'id': 1}, status=200)
        self.assertIn(b'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R', res.body)

    def test_fen_url_invalid_id(self):
        res = self.testapp.get('/fen', params={'id': 150}, status=200)
        self.assertIn(b'start', res.body)

    def test_edit_url_valid(self):
        res = self.testapp.get('/edit')
        self.assertIn(b'id_btn_start', res.body)
        self.assertIn(b'id_btn_clear', res.body)
        self.assertIn(b'id_btn_save', res.body)
        self.assertIn(b'id_text_area', res.body)
        self.assertIn(b'id_btn_flip', res.body)
        self.assertIn(b"var board = new ChessBoard('board', cfg);", res.body)

    def test_save_url(self):
        import json
        res = self.testapp.post_json('/save', dict(fen='r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP2PP/RNBQK2R'))
        self.assertIn(b'redirect', res.body)

    def test_save_url_fail(self):
        import json
        res = self.testapp.get('/save', dict(fen='r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP2PP/RNBQK2R'), status=404)
        self.assertIn(b'Not Found', res.body)
        self.assertEqual(res.status_int, 404)

    def test_list_url(self):
        res = self.testapp.get('/list')
        self.assertIn(b'width: 200px', res.body)

    def test_show_position(self):
        res = self.testapp.get('/positions', params={'id': 14})
        self.assertIn(b'board', res.body)

    def test_delete_position(self):
        res = self.testapp.delete(url='/delete/16')
        self.assertIn(b'redirect', res.body)
        self.assertEqual(res.status_int, 302)

    def test_delete_position_fail(self):
        res = self.testapp.get(url='/delete/16', status=404)
        self.assertIn(b'Not Found', res.body)
        self.assertEqual(res.status_int, 404)

    def test_play_position(self):
        res = self.testapp.get('/play?id=14')
        self.assertIn(b'board', res.body)
