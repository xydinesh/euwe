from pyramid.response import Response
from pyramid.exceptions import Forbidden
from pyramid.view import (view_config,
view_defaults)
from pyramid.security import (remember, forget, authenticated_userid)
from pyramid.httpexceptions import (
        exception_response,
        HTTPMethodNotAllowed,
        HTTPBadRequest,
        HTTPFound)
from .security import USERS
from .models import (DBSession, MyModel, PositionModel)
from sqlalchemy.exc import DBAPIError
import transaction

import logging
log = logging.getLogger(__name__)


@view_defaults(renderer='templates/welcome.mako')
class EuweViews(object):

    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='login', renderer='templates/login.mako')
    def login_view(self):
        """
        view for handling login
        """
        request = self.request
        login_url = request.route_url('login')
        referrer = request.url
        if referrer == login_url:
            referrer = '/list'

        came_from = request.params.get('came_from', referrer)
        message = ''
        username = 'username'
        password = 'password'

        if 'form.submitted' in request.params:
            username = request.params['username']
            password = request.params['password']
            if USERS.get(username) == password:
                headers = remember(request, username)
                return HTTPFound(location=came_from, headers=headers)

        message = 'Invalid Login, Try again'

        return dict(project='euwe', title='Euwe Login Page',
                url=request.application_url + '/login',
                came_from=came_from, message=message,
                username=username, password=password)

    @view_config(route_name='logout')
    def logout_view(self):
        request = self.request
        headers = forget(request)
        url = request.route_url('home')
        return HTTPFound(location=url, headers=headers)

    @view_config(route_name='fen')
    def fen_view(self):
        try:
            request = self.request
            userid = authenticated_userid(request)
            if userid is None:
                raise Forbidden()
            id = request.params.get('id', -1)
            pos = DBSession.query(PositionModel).filter_by(id=id).first()
        except DBAPIError:
            return Response(conn_err_msg, content_type='text/plain', status_int=500)
        return dict(project='euwe', position=pos, user=userid)

    @view_config(route_name='edit', renderer='templates/edit.mako')
    def edit_view(self):
        request = self.request
        userid = authenticated_userid(request)
        if userid is None:
            raise Forbidden()
        return dict(project='euwe', title='Euwe Edit Position',
                url=request.application_url + '/edit',
                message='', user=userid)

    @view_config(route_name='save', renderer='json', request_method=['POST'])
    def save_view(self):
        request = self.request
        userid = authenticated_userid(request)
        if userid is None:
            raise Forbidden()

        fen = request.json_body['fen']
        position = PositionModel(category='position', userid=userid, fen=fen)
        DBSession.add(position)
        position = DBSession.query(PositionModel).filter_by(fen=fen, userid=userid).first()

        url = request.route_url('list')
        return HTTPFound(location=url)

    @view_config(route_name='positions', renderer='templates/list.mako')
    @view_config(route_name='list', renderer='templates/list.mako')
    def list_view(self):
        request = self.request
        userid = authenticated_userid(request)
        if userid is None:
            raise Forbidden()

        id = request.params.get('id', None)
        if id is None:
            positions = DBSession.query(PositionModel).filter_by(userid=userid).all()
        else:
            positions = DBSession.query(PositionModel).filter_by(userid=userid, id=id).all()
        return dict(project='euwe', title='Euwe List Positions',
        message='', userid=userid, positions=positions)


    @view_config(route_name='delete', request_method=['DELETE'])
    def delete_view(self):
        request = self.request
        userid = authenticated_userid(request)
        if userid is None:
            raise Forbidden()

        came_from = request.params.get('came_from', '/list')
        id = request.matchdict.get('id', None)
        log.debug('id: {0}'.format(id))
        if id is None:
            raise HTTPBadRequest()
        else:
            position = DBSession.query(PositionModel).filter_by(userid=userid, id=id).first()
            log.debug('position {0}'.format(position))
            if position:
                DBSession.delete(position)
        url = '{0}?{1}'.format(request.route_url('list'), id)
        return HTTPFound(location=came_from)

    @view_config(route_name='play')
    def play_view(self):
        request = self.request
        userid = authenticated_userid(request)
        if userid is None:
            raise Forbidden()

        id = request.params.get('id', None)
        if id is not None:
            position = DBSession.query(PositionModel).filter_by(userid=userid, id=id).first()
        else:
            raise HTTPBadRequest()

        print (position)
        return dict(project='euwe', title='Euwe Play Position',
            message='', user=userid, position=position)


    @view_config(route_name='home')
    def my_view(self):
        try:
            request = self.request
            userid = authenticated_userid(request)
            if userid is None:
                raise Forbidden()
            one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
        except DBAPIError:
            return Response(conn_err_msg, content_type='text/plain', status_int=500)
        return {'one': one, 'project': 'euwe', 'user': userid}

    @view_config(route_name='hello', renderer='json')
    def hello_world(self):
        request = self.request
        userid = authenticated_userid(request)
        if userid is None:
            raise Forbidden()
        return Response('Hello %s!' % (userid,))

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_euwe_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
