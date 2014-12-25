from pyramid.response import Response
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.security import forget

from .security import USERS

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )

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
            referrer = '/'

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

    @view_config(route_name='home')
    def my_view(self):
        try:
            one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
        except DBAPIError:
            return Response(conn_err_msg, content_type='text/plain', status_int=500)
        return {'one': one, 'project': 'euwe'}


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
