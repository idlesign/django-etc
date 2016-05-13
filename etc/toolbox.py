from os import environ
from functools import partial
from collections import OrderedDict

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import module_has_submodule

try:
    from django.contrib.sites.shortcuts import get_current_site

except ImportError:  # Django < 1.7
    from django.contrib.sites.models import get_current_site

try:
    from django.apps import apps
    apps_get_model = apps.get_model

except ImportError:  # Django < 1.7
    from django.db.models import get_model
    apps_get_model = None

try:
    from django.utils.module_loading import import_module

except ImportError:
    # Django <=1.9.0
    from django.utils.importlib import import_module

from .utils import DomainGetter


def choices_list(*choices):
    """Helps to define choices for models, that could be addressed
    later as dictionaries.

    To be used in conjunction with `get_choices()`.

    Example:

        class MyModel(models.Model):

            TYPE_ONE = 1
            TYPE_TWO = 2

            TYPES = choices_list(
                (TYPE_ONE, 'Type one title'),
                (TYPE_TWO, 'Type two title'),
            )

            type = models.PositiveIntegerField('My type', choices=get_choices(TYPES), default=TYPE_TWO)

            def get_display_type(self):
                return self.TYPES[self.type]

    :param set|list choices:
    :rtype: OrderedDict
    :return: Choices ordered dictionary
    """
    return OrderedDict(choices)


def get_choices(choices_list):
    """Returns model field choices from a given choices list.
    Choices list is defined with `choices_list()`.

    :param OrderedDict choices_list:
    :rtype: tuple
    :return: Choices tuple
    """
    return tuple((key, val) for key, val in choices_list.items())


def set_form_widgets_attrs(form, attrs):
    """Applies a given HTML attributes to each field widget of a given form.

    Example:

        set_form_widgets_attrs(my_form, {'class': 'clickable'})

    """
    for _, field in form.fields.items():
        attrs_ = dict(attrs)
        for name, val in attrs.items():
            if hasattr(val, '__call__'):
                attrs_[name] = val(field)
        field.widget.attrs = field.widget.build_attrs(attrs_)


def get_model_class_from_string(model_path):
    """Returns a certain model as defined in a string formatted `<app_name>.<model_name>`.

    Example:

        model = get_model_class_from_string('myapp.MyModel')

    """
    try:
        app_name, model_name = model_path.split('.')
    except ValueError:
        raise ImproperlyConfigured('`%s` must have the following format: `app_name.model_name`.' % model_path)

    if apps_get_model is None:
        model = get_model(app_name, model_name)
    else:
        try:
            model = apps_get_model(app_name, model_name)
        except (LookupError, ValueError):
            model = None

    if model is None:
        raise ImproperlyConfigured('`%s` refers to a model `%s` that has not been installed.' % (model_path, model_name))

    return model


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
    return get_model_class_from_string(getattr(settings_module, settings_entry_name))


def get_site_url(request=None):
    """Tries to get a site URL from environment and settings
    in the following order:

    1. (SITE_PROTO / SITE_SCHEME) + SITE_DOMAIN
    2. SITE_URL
    3. Django Sites contrib
    4. Request object

    :param HttpRequest request: Request object to deduce URL from.
    :rtype: str

    """
    env = partial(environ.get)
    settings_ = partial(getattr, settings)

    domain = None
    scheme = None
    url = None

    for src in (env, settings_):
        if url is None:
            url = src('SITE_URL', None)

        if domain is None:
            domain = src('SITE_DOMAIN', None)

        if scheme is None:
            scheme = src('SITE_PROTO', src('SITE_SCHEME', None))

    if domain is None and url is not None:
        scheme, domain = url.split('://')[:2]

    if domain is None:
        site = get_current_site(request or DomainGetter(domain))
        domain = site.domain

    if scheme is None and request:
        scheme = request.scheme

    if domain is None:
        domain = 'undefined-domain.local'

    if scheme is None:
        scheme = 'http'

    domain = domain.rstrip('/')

    return '%s://%s' % (scheme, domain)


def import_app_module(app_name, module_name):
    """Returns a module from a given app by its name.

    :param str app_name:
    :param str module_name:
    :rtype: module or None

    """
    module = import_module(app_name)
    try:
        sub_module = import_module('%s.%s' % (app_name, module_name))
        return sub_module

    except:

        # The same bubbling strategy as in autodiscover_modules().
        if module_has_submodule(module, module_name):  # Module is in a package.
            raise

        return None


def import_project_modules(module_name):
    """Imports modules from registered apps using given module name
    and returns them as a list.

    :param str module_name:
    :rtype: list

    """
    from django.conf import settings

    submodules = []
    for app in settings.INSTALLED_APPS:
        module = import_app_module(app, module_name)
        if module is not None:
            submodules.append(module)

    return submodules
