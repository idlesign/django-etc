from pytest_djangoapp import configure_djangoapp_plugin


pytest_plugins = configure_djangoapp_plugin({
    'SITE_ID': 1,
    'INSTALLED_APPS': [
        'django.contrib.sites',
        'django.contrib.contenttypes',
        'django.contrib.auth',
    ],
})
