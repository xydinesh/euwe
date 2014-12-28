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

    # authentication and authorization
    authn_policy = AuthTktAuthenticationPolicy(settings['persona.secret'],
    callback=group_finder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

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
    config.scan()
    return config.make_wsgi_app()
