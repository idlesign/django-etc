from django import template

from ..toolbox import get_site_url

register = template.Library()


@register.simple_tag(takes_context=True)
def site_url(context):
    """Tries to get a site URL from environment and settings.

    See toolbox.get_site_url() for description.

    Example:

        {% load etc_misc %}
        {% site_url %}

    """
    return get_site_url(request=context.get('request', None))
