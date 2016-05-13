Various utils
=============


import_app_module
-----------------

**etc.toolbox.import_app_module** imports and returns a module from a specific app by its name.

If your application provides some kind of tooling for others and you know that configuration
for this tooling could be found in a certain module within a thirdparty app you can use this function
to load such a module by its name.

.. code-block:: python

    from etc.toolbox import import_app_module


    module = import_app_module('someapp', 'mymodule')  # Get `mymodule` module from `someapp` application.



import_project_modules
----------------------

**etc.toolbox.import_project_modules** imports modules from registered apps using given module name and returns them as a list.

This is an automation for `import_app_module()` described above to load all modules from every app in a project.


.. code-block:: python

    from etc.toolbox import import_project_modules


    all_modules = import_project_modules('mymodule')  # Get `mymodule` module from every app in a project.



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
