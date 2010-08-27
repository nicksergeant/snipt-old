# Django settings for snipt project.
import os.path

DEBUG = False

TEMPLATE_DEBUG = DEBUG

FORCE_LOWERCASE_TAGS = True

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'

ADMINS = ()

MANAGERS = ADMINS

DATABASE_ENGINE = ''            # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''         # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''  # Not used with sqlite3.sqlite3.
DATABASE_HOST = ''                   # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''                   # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_authopenid.middleware.OpenIDMiddleware',
    'pagination.middleware.PaginationMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'snipt.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

SESSION_COOKIE_AGE = 5259488

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.comments',
    'django.contrib.sites',
    'django_authopenid',
    'django_extensions',
    'piston',
    'snippet',
    'pagination',
    'compress',
    'snipt.ad',
    'snipt.api',
    'tagging',
    'favsnipt',
)

# cache requires these middleware items (in this order)
# 'django.middleware.cache.FetchFromCacheMiddleware',
# 'django.middleware.cache.UpdateCacheMiddleware',

# process: /usr/bin/memcached -m 64 -p 11211 -u nobody -l 127.0.0.1 
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
#CACHE_MIDDLEWARE_SECONDS = 600 # 10 mins
#CACHE_MIDDLEWARE_KEY_PREFIX = 'snipt' # set this if your cache is used across multiple sites
#CACHE_MIDDLEWARE_ANONYMOUS_ONLY = False # only shows cached stuff to non-logged-in users

COMMENTS_ALLOW_PROFANITIES = True

COMPRESS_VERSION = True
COMPRESS_CSS = {'all': {'source_filenames': ('style.css',), 'output_filename': 'snipt.r?.css'}}
COMPRESS_JS =  {'all': {'source_filenames': ('jquery.js','jquery.ui.js','jquery.autogrow.js','jquery.livequery.js','zero-clipboard.js','script.js',), 'output_filename': 'snipt.r?.js'}}

FIXTURE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'fixtures').replace('\\','/'),
)

# Override with settings in local_settings.py if it exists.
from local_settings import *
