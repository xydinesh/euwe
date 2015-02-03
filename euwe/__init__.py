from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .security import group_finder

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings,
                          root_factory='euwe.models.RootFactory')
    config.include('pyramid_mako')
    config.include('pyramid_persona')

    # static properties
    config.add_static_view('static', 'static', cache_max_age=60)
    config.add_static_view('img', 'static/img', cache_max_age=60)
    config.add_static_view('js', 'static/js', cache_max_age=60)

    # register views with routes
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('fen', '/fen')
    config.add_route('edit', '/edit')
    config.add_route('hello', '/hello')
    config.add_route('save', '/save')
    config.add_route('list', '/list')
    config.add_route('positions', '/positions')
    config.add_route('delete', '/delete/{id}')
    config.add_route('play', '/play')
    config.add_route('test', '/test')
    config.add_route('solution', '/solution')
    config.add_route('answer', '/answer')
    config.scan()
    return config.make_wsgi_app()
