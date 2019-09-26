# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')--manage.py change settings(live upload)
from .base import *

DEBUG = config('DEBUG', cast=bool)


ALLOWED_HOSTS = ['*','ip-address', 'www.your-website.com','your-website.com']


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS


if not DEBUG:
    loaders = [("django.template.loaders.cached.Loader", loaders)]

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),#IP Address that your DB is hosted on
        'PORT': ''
    }
}


EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
