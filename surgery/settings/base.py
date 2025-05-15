import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-8&w(uijh1twhv9$bgu7_if53cpm0gq0bq=o%jj6##y%1-hq658'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'apps.authentication',
    'apps.schedule',
]

MIDDLEWARE = [
    'core.middleware.authentication.JWTAuthenticationMiddleware',
    'core.middleware.request_middleware.RequestLogMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'surgery.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'surgery.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'EXCEPTION_HANDLER': 'core.common.exceptions.custom_exception_handler',
}

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

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

load_dotenv()
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY',
                           'GaeRXtfX3nbbK4tEGlmNuMsTV1J4s6Blrn8EEBerbWIIWbQAWCilrUrpDyzWXII2')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
# 七天
JWT_EXPIRATION_DELTA = int(os.getenv('JWT_EXPIRATION_DELTA', 60 * 60 * 24 * 7))

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1

# 日志配置
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/surgery.log'),
            'formatter': 'verbose',
            'encoding': 'UTF-8',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
        },
        'surgery': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
