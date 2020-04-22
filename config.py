import os
basedir = os.path.abspath(os.path.dirname(__file__))

'''
TODO: maybe if we have a db. Env vars in here
'''
class Config(object):
    DEBUG=True
    SECRET_KEY = ''
    DB_URI=''