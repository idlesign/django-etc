from django.utils import six

from .utils import InheritedModelMetaclass


class InheritedModel(six.with_metaclass(InheritedModelMetaclass)):
    """Mix in this class into target model (inherit from it) and define `Fields` class inside it
    to be able to customize field attributes (e.g. texts) of a base-parent model.


    Example:

        from etc.models import InheritedModel


        class MyParentModel(models.Model):

            code = models.CharField('dummy', max_length=64)
            expired = models.BooleanField('Expired', help_text='dummy')

            class Meta:
                abstract = True


        class MyChildModel1(InheritedModel, MyParentModel):  # NOTE: InheritedModel must go first.

            time_created = models.DateTimeField('Date created', auto_now_add=True)

            class Fields:  # Defining a class with fields custom fields data.
                code = 'Secret code'  # This is treated as verbose_name.
                expired = {'help_text': 'This code is expired.'}


        class MyChildModel2(InheritedModel, MyParentModel):

            code = models.CharField('dummy', max_length=128, unique=True, editable=False)

            class Fields:
                code = 'Non-secret code'
                expired = {'help_text': 'Do not check it. Do not.'}

    """
