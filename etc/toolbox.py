from functools import partial
from os import environ

from django.conf import settings

try:
    from django.contrib.sites.shortcuts import get_current_site

except ImportError:  # Django < 1.7
    from django.contrib.sites.models import get_current_site

from .choices import choices_list, get_choices
from .importing import import_app_module, import_project_modules
from .models import get_model_class_from_settings, get_model_class_from_string, InheritedModel
from .utils import DomainGetter


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
