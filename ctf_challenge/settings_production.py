import os
from .settings import *

# Override production settings here
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Host settings
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Secret key
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# Database settings remain SQLite for CTF (intentionally vulnerable)
# For a real production app, you would want to use PostgreSQL or MySQL

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# JWT settings - maintaining the vulnerable configuration for CTF
# In a real production app, these would be secured properly