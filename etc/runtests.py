#! /usr/bin/env python
import sys
import os

from django.conf import settings, global_settings


def main():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

    app_name = os.path.dirname(__file__)

    if not settings.configured:
        settings.configure(
            INSTALLED_APPS=('django.contrib.auth', 'django.contrib.contenttypes', app_name),
            DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
            MIDDLEWARE_CLASSES=global_settings.MIDDLEWARE_CLASSES,  # Prevents Django 1.7 warning.
        )

    try:  # Django 1.7 +
        from django import setup
        setup()
    except ImportError:
        pass

    from django.test.utils import get_runner
    runner = get_runner(settings)()
    failures = runner.run_tests((app_name,))

    sys.exit(failures)


if __name__ == '__main__':
    main()
