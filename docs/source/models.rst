Model Related Bits
==================


InheritedModel
--------------

**etc.toolbox.InheritedModel** allows to override fields attributes in inherited models.

Mix in this class into target model (inherit from it) and define `Fields` class inside it
to be able to customize field attributes (e.g. texts) of a base-parent model.


.. code-block:: python

    from etc.toolbox import InheritedModel


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



Template Tags
-------------

model_meta
~~~~~~~~~~

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


model_field
~~~~~~~~~~~

* **model_field_verbose_name** tag.

    Returns model field verbose name.

    .. code-block:: html

        {% load model_field %}
        {% model_field_verbose_name from my_model.fieldname %}


* **model_field_help_text** tag.

    Returns model field help text.

    .. code-block:: html

        {% load model_field %}
        {% model_field_help_text from my_model.fieldname %}


Both template tags are capable to redirect output into a template context variable using *as* clause. That could
be useful if you have a set of homogeneous objects (e.g. QuerySet or Page) and want to get verbose name just once:

.. code-block:: html

    {% model_field_verbose_name from my_models_set.fieldname as title_fieldname %}


.. note:: `fieldname` could be a literal field name or a template variable containing the name.


Getting models
--------------

get_model_class_from_string
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **etc.toolbox.get_model_class_from_string** allows getting model class from its string representation.

Returns a certain model as defined in a string formatted ``<app_name>.<model_name>``.

.. code-block:: python

        model = get_model_class_from_string('myapp.MyModel')



get_model_class_from_settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


Models choices
--------------

ChoicesEnumMixin
~~~~~~~~~~~~~~~~

**etc.toolbox.ChoicesEnumMixin** helps to define choices for models using ``Enum`` from Python 3.

Could be used in conjunction with ``get_choices`` for convenience.

.. code-block:: python

        from enum import Enum, unique

        @unique
        class Role(ChoicesEnumMixin, Enum):

            # Define your Enum with mixin:
            # Item values could be tuples: (value, title, hint).

            APPLICANT = 0, 'Title', 'Hint'
            ADMIN = 1, 'Administrator'
            MEMBER = 2

        class MyChoiceModel(models.Model):

            # Use the enum in field declaration.
            role = models.PositiveIntegerField(choices=get_choices(Role), default=Role.MEMBER)

        # Filter objects by enum values.
        members = MyChoiceModel.objects.filter(role=Role.MEMBER)

        # Access titles and hints registries
        # (ordered dictionaries, indexed by values):
        titles = Role.titles
        hints = Role.hints


choices_list
~~~~~~~~~~~~

**etc.toolbox.choices_list** helps to define choices for models, that could be addressed later as dictionaries.

To be used in conjunction with ``get_choices``.

.. code-block:: python

    class MyModel(models.Model):

        TYPE_ONE = 1
        TYPE_TWO = 2

        TYPES = choices_list(
            (TYPE_ONE, 'Type one title'),
            (TYPE_TWO, 'Type two title'),
        )

        type = models.PositiveIntegerField('My type', choices=get_choices(TYPES), default=TYPE_TWO)

        def get_display_type(self):
            return self.TYPES[self.type]


get_choices
~~~~~~~~~~~

**etc.toolbox.get_choices** returns model field choices from a given choices list.

Choices list is defined with ``choices_list`` or ``ChoicesEnumMixin``, see above.
