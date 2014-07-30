Models Related Bits
===================


InheritedModel Model
--------------------

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

