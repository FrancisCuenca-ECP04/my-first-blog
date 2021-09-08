import os

DJAGO_SECRET_KEY="10d4dfd0e671dfe3939996fbb853a054bd6ee65c"
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True