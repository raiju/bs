# -*- coding: utf-8 -*-
"""Setup the bs application"""

import logging
from tg import config
import transaction


def setup_schema(command, conf, vars):
    """Place any commands to setup bs here"""
    # Load the models

    # <websetup.websetup.schema.before.model.import>
    from bs import model
    # <websetup.websetup.schema.after.model.import>

    # <websetup.websetup.schema.before.metadata.create_all>
    print "[bs] Creating tables"
    model.metadata.create_all(bind=config['pylons.app_globals'].sa_engine)
    # <websetup.websetup.schema.after.metadata.create_all>
    transaction.commit()
    from migrate.versioning.shell import main
    from migrate import exceptions
    try:
        main(argv=['version_control'], url=config['sqlalchemy.url'], repository='migration', name='migration')
    except exceptions.DatabaseAlreadyControlledError:
        print '[bs-ignore-error] Database already under version control'
    except exceptions.InvalidRepositoryError:
        print '[bs-ignore-error] Invalid repository'
