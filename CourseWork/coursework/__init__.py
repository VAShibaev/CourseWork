from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Everyone, Authenticated

from .models import (
    University,
    Article,
    Article_Author,
    Journal,
    User,
    Author
    )


class MyFactory(object):
    def __init__(self, request):
        self.__acl__ = [
                (Allow, Everyone, 'view'),
 #               (Allow, 'admin', ('add', 'delete', 'edit', 'move'))
            ]

def sacrud_settings(config):
    config.include('pyramid_sacrud', route_prefix='admin')
    config.registry.settings['pyramid_sacrud.models'] = (
        ('Group1', [User]),
        ('Group2', [Author]),
        ('Group3', [Journal]),
        ('Group4', [Article_Author]),
        ('Group5', [Article]),
        ('Group6', [University])
    )
        

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    
    config = Configurator(settings=settings, root_factory=MyFactory)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    
    config.include('pyramid_chameleon')
    config.include('pyramid_sqlalchemy')
    config.include('pyramid_jinja2')
    config.include(sacrud_settings)
    
    config.add_static_view('static', 'static')
    config.add_static_view('uploads','files')
    config.add_route('home', '/')
    config.add_route('article','/article/{id:\d+}')
    config.add_route('file','/file/{id:\d+}')
    config.add_route('login','/login')
    config.add_route('logout','/logout')
    config.add_route('registration','/registration')
    config.add_route('addarticle','/addarticle')
    
    config.scan()
    return config.make_wsgi_app()
