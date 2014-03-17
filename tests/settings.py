SECRET_KEY = "No More DeprecationWarnings"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'grass.db',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'autocomplete_light',
    'grass',
    'demo',
]

SITE_ID = 1
ROOT_URLCONF = 'demo.urls'
