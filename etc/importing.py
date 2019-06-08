from django.utils.module_loading import module_has_submodule

try:
    from django.utils.module_loading import import_module

except ImportError:
    # Django <=1.9.0
    from django.utils.importlib import import_module


def import_app_module(app_name, module_name):
    """Returns a module from a given app by its name.

    :param str app_name:
    :param str module_name:
    :rtype: module or None

    """
    name_split = app_name.split('.')
    if name_split[-1][0].isupper():  # Seems that we have app config class path here.
        app_name = '.'.join(name_split[:-2])

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
