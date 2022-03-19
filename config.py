from datetime import timedelta
import secrets
import os.path


basedir = os.path.abspath(os.path.dirname(__file__))
secret_key = secrets.token_hex()

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'main.db')
#SQLALCHEMY_DATABASE_URI = 'mysql://teste:teste1234@teste.tk/flaskblue'

SQLALCHEMY_TRACK_MODIFICATIONS = False

#USE_SESSION_FOR_NEXT = True
REMEMBER_COOKIE_DURATION = timedelta(days=7)

THREADS_PER_PAGE = 2

CSRF_ENABLED = True
CSRF_SESSION_KEY = 'secret'

SECRET_KEY = secret_key