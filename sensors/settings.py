""" Microservice configurator file """
##
#
# This file configures the microservice.
#
# This microservice uses 'dotenv' (.env) files to get environmental variables.
# This is done to configure sensible parameters, like database connections,
# application secret keys and the like. In case the 'dotenv' file does not
# exists, a warning is generated at run-time.
#
# This application implements the '12 Factor App' principle:
# https://12factor.net and https://12factor.net/config
#
# Note about PyLint static code analyzer: items disable are false positives.
#
##

# pylint: disable=too-few-public-methods;
# In order to avoid false positives with Flask

from os import environ, path
from environs import Env


ENV_FILE = path.join(path.abspath(path.dirname(__file__)), '.env')

if path.exists(ENV_FILE):
    ENVIR = Env()
    ENVIR.read_env()
else:
    print('Error: .env file not found')
    exit(code=1)


class Config:
    """ This is the generic loader that sets common attributes """
    JSON_SORT_KEYS = False
    DEBUG = True
    TESTING = True


class Development(Config):
    """ Development loader """
    ENV = 'development'
    if environ.get('KEY_DEVL'):
        SECRET_KEY = ENVIR('KEY_DEVL')
    if environ.get('DATABASE_URI_DEVL'):
        DATABASE_URI = ENVIR('DATABASE_URI_DEVL')
    TESTING = False


class Testing(Config):
    """ Testing loader """
    ENV = 'testing'
    if environ.get('KEY_TEST'):
        SECRET_KEY = ENVIR('KEY_TEST')
    if environ.get('DATABASE_URI_TEST'):
        DATABASE_URI = ENVIR('DATABASE_URI_TEST')
    DEBUG = False


class Production(Config):
    """ Production loader """
    ENV = 'production'
    if environ.get('KEY_PROD'):
        SECRET_KEY = ENVIR('KEY_PROD')
    if environ.get('DATABASE_URI_PROD'):
        DATABASE_URI = ENVIR('DATABASE_URI_PROD')
    DEBUG = False
    TESTING = False
