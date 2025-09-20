from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'flowc_db',  # Replace with your database name
            'USER': 'postgres',  # Replace with your PostgreSQL username
            'PASSWORD': '1234', # Replace with your password
            'HOST': 'localhost',  # Or the IP address/hostname of your PostgreSQL server
            'PORT': '5432',  # Default PostgreSQL port
        }
}