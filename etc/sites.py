from functools import partial
from os import environ

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


class DomainGetter(object):

    __slots__ = ['domain']

    def __init__(self, domain):
        self.domain = domain

    def get_host(self):
        return self.domain


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
