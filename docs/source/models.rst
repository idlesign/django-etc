Models Related Bits
===================


InheritedModel
--------------

**etc.models.InheritedModel** allows to override fields attributes in inherited models.

Mix in this class into target model (inherit from it) and define `Fields` class inside it
to be able to customize field attributes (e.g. texts) of a base-parent model.


.. code-block:: python

    from etc.models import InheritedModel


    class MyAbstractModel(models.Model):

        code = models.CharField('dummy', max_length=64)
        expired = models.BooleanField('Expired', help_text='dummy')

        class Meta:
            abstract = True


    class SecretModel(InheritedModel, MyParentModel):  # NOTE: InheritedModel must go first.

        time_created = models.DateTimeField('Date created', auto_now_add=True)

        class Fields:  # Defining a class with fields custom fields data.
            code = 'Secret code'  # This is treated as verbose_name.
            expired = {'help_text': 'This code is expired.'}


    class NonSecretModel(InheritedModel, MyParentModel):

        code = models.CharField('dummy', max_length=128, unique=True, editable=False)

        class Fields:
            code = 'Non-secret code'
            expired = {'help_text': 'Do not check it. Do not.'}



`model_meta` Template Tags
--------------------------

* **model_meta_verbose_name** tag.

    Returns model verbose name singular.

    .. code-block:: html

        {% load model_meta %}
        {% model_meta_verbose_name my_model %}


* **model_meta_verbose_name_plural** tag.

    Returns model verbose name plural.

    .. code-block:: html

        {% load model_meta %}
        {% model_meta_verbose_name_plural my_model %}


get_model_class_from_settings
-----------------------------

**etc.toolbox.get_model_class_from_settings** allows getting model class from its string representation in settings module.

This might be handy if you allow users of your app to extend/override your built-in models:

.. code-block:: python

        myapp/settings.py

            from django.conf import settings

            # This allows users to set MYAPP_MY_MODEL in settings.py of their projects.
            MY_MODEL = getattr(settings, 'MYAPP_MY_MODEL', 'myapp.MyModel')


        myapp/utils.py

            from myapp import settings

            def get_my_model():
                return get_model_class_from_settings(settings, 'MY_MODEL')


After that ``get_my_model`` will always return an appropriate model class object even if it is customized by a user.
