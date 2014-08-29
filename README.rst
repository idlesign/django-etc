django-etc
==========
https://github.com/idlesign/django-etc

.. image:: https://badge.fury.io/py/django-etc.png
    :target: http://badge.fury.io/py/django-etc

.. image:: https://pypip.in/d/django-etc/badge.png
        :target: https://crate.io/packages/django-etc


Description
-----------

*Tiny stuff for Django that won't fit into separate apps.*


Models:

* **etc.models.InheritedModel** allows to override fields attributes in inherited models.

* **etc.toolbox.get_model_class_from_settings** allows getting model class from its string representation in settings module.


Forms:

* **etc.toolbox.set_form_widgets_attrs** allows bulk apply HTML attributes to every field widget of a given form.


Template tags:

* `model_meta`:

    * **model_meta_verbose_name** returns model verbose name singular.

    * **model_meta_verbose_name_plural** returns model verbose name plural.

* `gravatar`

    * **gravatar_get_url** returns Gravatar image URL for a given string or UserModel.

    * **gravatar_get_img** returns Gravatar image HTML tag for a given string or UserModel.



Documentation
-------------

http://django-etc.readthedocs.org/
