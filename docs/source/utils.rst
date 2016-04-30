Various utils
=============


get_site_url
------------

**etc.toolbox.get_site_url** does its best to provide you with a site URL where request object is unavailable.

On occasions when you do not have a request object to get current site URL from (e.g. background tasks)
this function tries to get it from *environment* and *settings*, using the following order:

1. (SITE_PROTO or SITE_SCHEME) + SITE_DOMAIN
2. SITE_URL
3. Django Sites contrib
4. Request object (if available)


.. code-block:: python

    from etc.toolbox import get_site_url


    my_url = get_site_url()



`etc_misc` Template Tags
------------------------

* **site_url** tag.

    Does its best to provide you with a site URL whether request object is unavailable or not.
    See ``get_site_url`` description above.

    .. code-block:: html

        {% load etc_misc %}
        {% site_url %}
