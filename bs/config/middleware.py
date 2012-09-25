# -*- coding: utf-8 -*-

"""WSGI middleware initialization for the bs application."""



from bs.config.app_cfg import base_config

from bs.config.environment import load_environment

from repoze.who.config import make_middleware_with_config

import tw2.core as twc

__all__ = ['make_app']



# Use base_config to setup the necessary PasteDeploy application factory. 

# make_base_app will wrap the TG2 app with all the middleware it needs. 

make_base_app = base_config.setup_tg_wsgi_app(load_environment)





def make_app(global_conf, full_stack=True, **app_conf):

    """
    Set bs up with the settings found in the PasteDeploy configuration
    file used.
    :param global_conf: The global settings for bs (those
        defined under the ``[DEFAULT]`` section).
    :type global_conf: dict
    :param full_stack: Should the whole TG2 stack be set up?
    :type full_stack: str or bool
    :return: The bs application with all the relevant middleware
        loaded.

    This is the PasteDeploy factory for the bs application.
    ``app_conf`` contains all the application-specific settings (those defined
    under ``[app:main]``.
    """

    custom = lambda app : twc.make_middleware(app, default_engine='mako')
    app = make_base_app(global_conf, wrap_app=custom, full_stack=True, **app_conf)
    #app = make_base_app(global_conf, full_stack=True, **app_conf)
    # Wrap your base TurboGears 2 application with custom middleware here
    # This custom middleware is about authentication
    app = make_middleware_with_config(
        app,
        global_conf,
        app_conf.get('who.config_file','who.ini'),
        app_conf.get('who.log_file','auth.log'),
        app_conf.get('who.log_level','debug')
    )


    return app


