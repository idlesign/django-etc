# Quickstart

Install the package:

```shell
$ python -m pip install django-etc
```

Add the **etc** application to `INSTALLED_APPS` in your settings file:

```python
INSTALLED_APPS = [
    # ...
    'etc',
]
```

You are ready to use the utilities, e.g.:

```python
from etc.toolbox import get_site_url


my_url = get_site_url()
```

See the following sections for the details:

- [Model related bits](020_models.md)
- [Tools for Django Admin](030_admin.md)
- [Forms related bits](040_forms.md)
- [Various utils](050_utils.md)
- [Thirdparty related bits](060_thirdparty.md)
