django-etc
==========
https://github.com/idlesign/django-etc

.. image:: https://img.shields.io/pypi/v/django-etc.svg
    :target: https://pypi.python.org/pypi/django-etc

.. image:: https://img.shields.io/pypi/l/django-etc.svg
    :target: https://pypi.python.org/pypi/django-etc

.. image:: https://img.shields.io/coveralls/idlesign/django-etc/master.svg
    :target: https://coveralls.io/r/idlesign/django-etc


Description
-----------

*Tiny stuff for Django that won't fit into separate apps.*


Utils
~~~~~

* **etc.toolbox.get_site_url** does its best to provide you with a site URL whether request object is available or not.

* **etc.toolbox.import_app_module** imports and returns a module from a specific app by its name.

* **etc.toolbox.import_project_modules** imports modules from registered apps using given module name and returns them as a list.


Models
~~~~~~

* **etc.toolbox.InheritedModel** allows to override fields attributes in inherited models.

* **etc.toolbox.get_model_class_from_string** allows getting model class from its string representation.

* **etc.toolbox.get_model_class_from_settings** allows getting model class from its string representation in settings module.

* **etc.toolbox.ChoicesEnumMixin** helps to define choices for models using ``Enum`` from Python 3.

* **etc.toolbox.choices_list** helps to define choices for models, that could be addressed later as dictionaries.

* **etc.toolbox.get_choices** returns model field choices from a given choices list.


Admin
~~~~~

* **etc.admin.CustomModelPage** allows easy construction of custom admin pages processing user input.


Forms
~~~~~

* **etc.toolbox.set_form_widgets_attrs** allows bulk apply HTML attributes to every field widget of a given form.


Template tags
~~~~~~~~~~~~~

* ``model_field``:

  * **model_field_verbose_name** returns model field verbose name.

  * **model_field_help_text** returns model field help text.

* ``model_meta``:

  * **model_meta_verbose_name** returns model verbose name singular.

  * **model_meta_verbose_name_plural** returns model verbose name plural.

* ``gravatar``

  * **gravatar_get_url** returns Gravatar image URL for a given string or UserModel.

  * **gravatar_get_img** returns Gravatar image HTML tag for a given string or UserModel.

* ``etc_misc``

  * **site_url** does its best to provide you with a site URL whether request object is available or not.

  * **include_** allows a template name to include template variables. Allows fallback template if the target is not found.



Documentation
-------------

http://django-etc.readthedocs.org/
