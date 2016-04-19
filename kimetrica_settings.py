from common import *  # nopep8

# this setting file will not work on "runserver" -- it needs a server for
# static files
DEBUG = True

# override to set the actual location for the production static and media
# directories
MEDIA_ROOT = '/kobocat/formhub-media'
STATIC_ROOT = "/kobocat/formhub-static"
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "static"),
)
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
# your actual production settings go here...,.
DATABASES = {
    'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'formhub',
        'USER': 'formhub_prod',
        # the password must be stored in an environment variable
        'PASSWORD': 'lahWuib2kohDiekeiX6z',
        # the server name may be in env
        'HOST': 'postgresql',
        # Replacement for TransactionMiddleware
        'ATOMIC_REQUESTS': True,
    },
    'gis': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'phis',
        'USER': 'staff',
        # the password must be stored in an environment variable
        'PASSWORD': 'oke2ooJ7ooz1Wude0tho',
        'HOST': 'postgis',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Africa/Lagos'

TOUCHFORMS_URL = 'http://localhost:8000/'
ENKETO_URL = 'http://localhost:8005'
# specifically for site urls sent to enketo
ENKETO_PROTOCOL = os.environ.get('ENKETO_PROTOCOL', 'http')
ENKETO_API_TOKEN = 'enketorules'


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'mlfs33^s1l4xf6a36$0#j%dd*sisfo6HOktYXB9y'

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

MIDDLEWARE_CLASSES += ('django.middleware.cache.UpdateCacheMiddleware',
                       'django.middleware.common.CommonMiddleware',
                       'django.middleware.cache.FetchFromCacheMiddleware',)

CACHE_MIDDLEWARE_SECONDS = 3600  # 1 hour
CACHE_MIDDLEWARE_KEY_PREFIX = ''


MONGO_DATABASE = {
    'HOST': os.environ.get('KOBOCAT_MONGO_HOST', 'mongo'),
    'PORT': int(os.environ.get('KOBOCAT_MONGO_PORT', 27017)),
    'NAME': os.environ.get('KOBOCAT_MONGO_NAME', 'formhub'),
    'USER': os.environ.get('KOBOCAT_MONGO_USER', ''),
    'PASSWORD': os.environ.get('KOBOCAT_MONGO_PASS', '')
}

# MongoDB - moved here from common.py
if MONGO_DATABASE.get('USER') and MONGO_DATABASE.get('PASSWORD'):
    MONGO_CONNECTION_URL = (
        "mongodb://%(USER)s:%(PASSWORD)s@%(HOST)s:%(PORT)s") % MONGO_DATABASE
else:
    MONGO_CONNECTION_URL = "mongodb://%(HOST)s:%(PORT)s" % MONGO_DATABASE

MONGO_CONNECTION = MongoClient(
    MONGO_CONNECTION_URL, safe=True, j=True, tz_aware=True)
MONGO_DB = MONGO_CONNECTION[MONGO_DATABASE['NAME']]


TESTING_MODE = False


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.gis',
    'registration',
    'reversion',
    'django_digest',
    'corsheaders',
    'oauth2_provider',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'taggit',
    'readonly',
    'onadata.apps.logger',
    'onadata.apps.viewer',
    'onadata.apps.main',
    'onadata.apps.restservice',
    'onadata.apps.api',
    'guardian',
    'djcelery',
    'onadata.apps.stats',
    'onadata.apps.sms_support',
    'onadata.libs',
)


# this undocumented setting uses different templates and static files
TEMPLATE_OVERRIDE_ROOT_DIR = '/kobocat/kobocat-template'

if isinstance(TEMPLATE_OVERRIDE_ROOT_DIR, basestring):
    # site templates overrides
    TEMPLATE_DIRS = (
        os.path.join(PROJECT_ROOT, TEMPLATE_OVERRIDE_ROOT_DIR, 'templates'),
    ) + TEMPLATE_DIRS
    # site static files path
    STATICFILES_DIRS += (
        os.path.join(PROJECT_ROOT, TEMPLATE_OVERRIDE_ROOT_DIR, 'static'),
    )

ENKETO_API_INSTANCE_IFRAME_URL = 'http://localhost:8005/api_v1/instance/iframe'
ENKETO_PREVIEW_URL = 'http://localhost:8005/preview'


REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
    'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'onadata.libs.authentication.DigestAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        # disabling this temporarily to prevent error while testing:
        # "Using basic authentication without HTTPS transmits credentials in
        # clear text! You MUST connect via HTTPS to use basic authentication."
#         'onadata.libs.authentication.HttpsOnlyBasicAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        # Keep JSONRenderer at the top "in order to send JSON responses to
        # clients that do not specify an Accept header." See
        # http://www.django-rest-framework.org/api-guide/renderers/#ordering-of-renderer-classes
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_jsonp.renderers.JSONPRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    ),
    'VIEW_NAME_FUNCTION': 'onadata.apps.api.tools.get_view_name',
    'VIEW_DESCRIPTION_FUNCTION': 'onadata.apps.api.tools.get_view_description',
}
