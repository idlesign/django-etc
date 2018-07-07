from django.db import models

from etc.models import InheritedModel


class MyParentModel(models.Model):

    code = models.CharField('dummy', max_length=64)
    expired = models.BooleanField('Expired', help_text='dummy', default=False)

    class Meta:
        abstract = True


class MyChildModel1(InheritedModel, MyParentModel):

    class Fields:
        code = 'Secret code'
        expired = {'help_text': 'This code is expired.'}

    class Meta:
        verbose_name = 'Verb'
        verbose_name_plural = 'VerbPlural'


class MyChildModel2(InheritedModel, MyParentModel):

    class Fields:
        code = 'Non-secret code'
