import os

class Config(object):
    GREETING = 'Welcome to the Index'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-key-for-devs'