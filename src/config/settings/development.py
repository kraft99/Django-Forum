 # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development') -- manage.py change settings
from .base import *

DEBUG = True


ALLOWED_HOSTS = config('ALLOWED_HOSTS',
						cast=lambda x:[s.strip() for s in x.split(',')],
						default='127.0.0.1,localhost')

# Debug_toolbar 
INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS += ['debug_toolbar',]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Debug Toolbar settings
DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]

def reveal_toolbar(request):
	return True

DEBUG_TOOLBAR_CONFIG = {
	"INTERCEPT_REDIRECTS": False,
	"SHOW_TOOLBAR_CALLBACK": reveal_toolbar
}



"""
@purpose - testing email providers in development only
@use - console or file (with provided email storage)

with console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


with file
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "emails")

"""

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "emails")