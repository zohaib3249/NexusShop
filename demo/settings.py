import os

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'django_countries',
    'core'
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]
ACCOUNT_FORMS = {'signup': 'core.forms.CustomSignupForm'}

ROOT_URLCONF = 'demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.sendEmail',
            ],
        },
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LANGUAGES = [
    ('ro', ('Romanian')),
    ('en', ('English')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR,'locale')
]
# static files (CSS, JS, Image)

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_URL = '/media_root/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')
#MEDIA_ROOT = BASE_DIR / "media_root"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

if ENVIRONMENT == 'production':
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Auth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '123',
            'secret': '456',
            'key': '666'
        }
    }
}

# CRISPY FORM

CRISPY_TEMPLATE_PACK = 'bootstrap4'

STRIPE_PUBLIC_KEY = 'pk_test_51LDsugJgULk81CRcMjbomvxv9WAX192uqfd7jx0YAFWyuP9hEdjgH4FYfo2jG6DdoxrcLN3LtE6ISm0esLjZzOlT00EX850iXS'
STRIPE_SECRET_KEY = 'sk_test_51LDsugJgULk81CRcuFJ87OirGsaFVbCWES0CVkNZMispvTPongrLeSnDDMb27yr1cgAmsYVpMqKzsyi1PBeDPT8s00N0C6Flsg'

"""
STRIPE_PUBLIC_KEY = 'pk_test_51LDtAOK4zvHCXzEsCWlPgJL7dix0IkvKlQifeaVwaHhLc7RYSmbySqm4es6kzwed6HuXsaPrN235HsT7hE8Dd3yo007UWsvgQb'
STRIPE_SECRET_KEY = 'sk_test_51LDtAOK4zvHCXzEsMNWOGlqLkBOgtPLmVnmqV28mtxxCIGI78MRcPOII5uHcVC6wUgOWkIqAC5oEiemreDgz1WUR00eGsD6lys'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'selfstudyjo@gmail.com'
EMAIL_HOST_PASSWORD ='mxlypxacktxzaffz'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'easyfilesforu@gmail.com'
EMAIL_HOST_PASSWORD = 'rkciaonksgveyxor'
s="pk_test_51LDsugJgULk81CRcMjbomvxv9WAX192uqfd7jx0YAFWyuP9hEdjgH4FYfo2jG6DdoxrcLN3LtE6ISm0esLjZzOlT00EX850iXS"
sk="sk_test_51LDsugJgULk81CRcuFJ87OirGsaFVbCWES0CVkNZMispvTPongrLeSnDDMb27yr1cgAmsYVpMqKzsyi1PBeDPT8s00N0C6Flsg"
