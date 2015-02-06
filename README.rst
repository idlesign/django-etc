django-etc
==========
https://github.com/idlesign/django-etc

.. image:: https://badge.fury.io/py/django-etc.png
    :target: http://badge.fury.io/py/django-etc

.. image:: https://pypip.in/d/django-etc/badge.png
        :target: https://crate.io/packages/django-etc

.. image:: https://coveralls.io/repos/idlesign/django-etc/badge.png
    :target: https://coveralls.io/r/idlesign/django-etc

.. image:: https://travis-ci.org/idlesign/django-etc.svg?branch=master
    :target: https://travis-ci.org/idlesign/django-etc


Description
-----------

*Tiny stuff for Django that won't fit into separate apps.*


Utils:

* **etc.toolbox.get_site_url** does its best to provide you with a site URL where request object is unavailable.


Models:

* **etc.models.InheritedModel** allows to override fields attributes in inherited models.

* **etc.toolbox.get_model_class_from_string** allows getting model class from its string representation.

* **etc.toolbox.get_model_class_from_settings** allows getting model class from its string representation in settings module.

* **etc.toolbox.choices_list** helps to define choices for models, that could be addressed later as dictionaries.

* **etc.toolbox.get_choices** returns model field choices from a given choices list.


Forms:

* **etc.toolbox.set_form_widgets_attrs** allows bulk apply HTML attributes to every field widget of a given form.


Template tags:

* `model_field`:

    * **model_field_verbose_name** returns model field verbose name.

    * **model_field_help_text** returns model field help text.

* `model_meta`:

    * **model_meta_verbose_name** returns model verbose name singular.

    * **model_meta_verbose_name_plural** returns model verbose name plural.

* `gravatar`

    * **gravatar_get_url** returns Gravatar image URL for a given string or UserModel.

    * **gravatar_get_img** returns Gravatar image HTML tag for a given string or UserModel.



Documentation
-------------

http://django-etc.readthedocs.org/
