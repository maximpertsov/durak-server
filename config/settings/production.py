import os

import dj_database_url
from config.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ["xdurak.herokuapp.com"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# Database
DATABASES = {"default": dj_database_url.config(conn_max_age=600)}

# CORS configuration
CLIENT_DOMAIN = os.environ["CLIENT_DOMAIN"]
CORS_ORIGIN_WHITELIST = ["https://{}".format(CLIENT_DOMAIN)]
