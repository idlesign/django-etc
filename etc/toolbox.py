from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model


def get_model_class_from_settings(settings_module, settings_entry_name):
    """Returns a certain model as defined in a given settings module.

    Example:

        myapp/settings.py

            from django.conf import settings

            MY_MODEL = getattr(settings, 'MYAPP_MY_MODEL', 'myapp.MyModel')


        myapp/some.py

            from myapp import settings

            model = get_model_class_from_settings(settings, 'MY_MODEL')

    """
    try:
        app_name, model_name = getattr(settings_module, settings_entry_name).split('.')
    except ValueError:
        raise ImproperlyConfigured('`%s` must have the following format: `app_name.model_name`.' % settings_entry_name)

    model = get_model(app_name, model_name)

    if model is None:
        raise ImproperlyConfigured('`%s` refers to a model `%s` that has not been installed.' % (settings_entry_name, model_name))

    return model

