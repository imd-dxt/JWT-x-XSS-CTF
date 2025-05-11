import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-i83$f%2@#_hs&^s0@6!+-l5g2$k@ml^!7(itd^95z$9ij4s@dg')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(BASE_DIR, 'staticfiles'))

# Create the static directory if it doesn't exist
os.makedirs(STATIC_ROOT, exist_ok=True)

# Make sure STATICFILES_DIRS points to existing directories
STATICFILES_DIRS = []
if os.path.exists(os.path.join(BASE_DIR, 'static')):
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))

# Create the media directory if it doesn't exist
os.makedirs(MEDIA_ROOT, exist_ok=True)