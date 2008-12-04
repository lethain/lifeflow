# LifeFlow specific settings

LIFEFLOW_KEYWORDS = "Blog Will Larson Programming Life"
LIFEFLOW_DESCRIPTION = "Will Larson's blog about programming and other things."
LIFEFLOW_AUTHOR_NAME = "Will Larson"
LIFEFLOW_BLOG_NAME = "Irrational Exuberance"
LIFEFLOW_CUSTOM_CSS = "/media/lifeflow/skins/lethain_neue.css"
LIFEFLOW_USE_PROJECTS = True
LIFEFLOW_CUSTOM_JS_HEADER = None
LIFEFLOW_CUSTOM_JS_FOOTER = None
LIFEFLOW_GOOGLE_ANALYTICS_ID = "UA-1812785-2"
LOGIN_URL = u"/editor/login/"
LOGOUT_URL = u"/editor/logout/"
LOGIN_REDIRECT_URL = "/editor/"
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "lifeflow.context.blog",
)
INSTALLED_APPS = (
    'lifeflow_core',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.markup',
)

# standard stuff
import os
ROOT_PATH = os.path.dirname(__file__)
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = os.path.join(ROOT_PATH, "media")
MEDIA_URL = 'http://127.0.0.1:8000/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'
CACHE_BACKEND="locmem:///"
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(ROOT_PATH,'db.db')
MEDIA_URL = 'http://127.0.0.1:8000/media/'
MEDIA_ROOT = os.path.join(ROOT_PATH,'media')
ADMIN_MEDIA_PREFIX = '/media/admin/'
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'aaaaa23f1tkf4opkfpokfw'
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.cache.CacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.doc.XViewMiddleware',
)
ROOT_URLCONF = 'example_project.urls'
TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, "templates")
)

try:
    from local_settings import *
except ImportError:
    pass
