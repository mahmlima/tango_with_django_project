"""
Django settings for tango_with_django_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j3jwltt(uw%3!+v$pgo2r=hf*qbhd+_97vj65m8xb3&_er%1oz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

LOGIN_URL = '/rango/longin/'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rango',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tango_with_django_project.urls'

WSGI_APPLICATION = 'tango_with_django_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


#Added by marina
SETTINGS_DIR = os.path.dirname(__file__)

PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)

#If you're planying on put the /template directory inside each app directory, this line won't be needed:
#Doing that, it is necessary to create another variable for static and media files, since they are in the root directory.
PROJECT_PATH = os.path.abspath(PROJECT_PATH)

TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')

TEMPLATE_DIRS = (
        TEMPLATE_PATH,
    )

STATIC_PATH = os.path.join(PROJECT_PATH, 'static')

STATICFILES_DIRS = (
    STATIC_PATH,
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

DATABASE_PATH = os.path.join(PROJECT_PATH, 'rango.db')


# SETTINGS_PATH = os.path.normpath(os.path.dirname(__file__))

# DATABASE_PATH = os.path.join(SETTINGS_PATH, 'rango.db')





# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


