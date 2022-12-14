"""
Django settings for prototyping project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

from django.contrib.messages import constants as messages
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yyy-#wnrjp9ek9+1t0!gj!=o!=^!7438hqe54_%m!&$6w^+mk$'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'article.apps.ArticleConfig',
    'accounts.apps.AccountsConfig',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'prototyping.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'prototyping.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'private_diary',
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': '',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'


#??????????????????????????????????????????
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

#???????????????????????????
MESSAGE_TAGS = {
    messages.ERROR: 'bg-danger',
    messages.WARNING: 'bg-warning',
    messages.SUCCESS: 'bg-success',
    messages.INFO: 'bg-info',
}

#??????????????????????????????????????????
AUTH_USER_MODEL = 'accounts.CustomUser'

#django-allauth???????????????django.contrib.auth.sites????????????????????????????????????ID?????????
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    #??????????????????(???????????????????????????)
    'django.contrib.auth.backends.ModelBackend',
    #??????????????????(??????????????????)
)

#????????????????????????????????????????????????
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False

#????????????????????????????????????????????????????????????????????????
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True

#????????????/??????????????????????????????????????????
LOGIN_REDIRECT_URL = 'article:index'
ACCOUNT_LOGOUT_REDIRECT_URL = 'article:index'

#???????????????????????????????????????????????????????????????????????????
ACCOUNT_LOGOUT_ON_GET = True

#?????????????????????URL?????????????????????????????????URL?????????
MEDIA_URL = '/media/'

#?????????????????????????????????
BACKUP_PATH = 'backup/'
NUM_SAVED_BACKUP = 30

#allauth????????????css???form?????????
ACCOUNT_FORMS = {
    'login' : 'accounts.forms.MyLoginForm',
    'signup' : 'accounts.forms.MySignupForm',
    'password_reset_from_key' : 'accounts.forms.MyPasswordResetFromKeyForm',
    'password_reset' : 'accounts.forms.MyPasswordResetForm',
}