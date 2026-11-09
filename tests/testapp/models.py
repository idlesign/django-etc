from sys import version_info
from django.db import models

from etc.toolbox import InheritedModel


if version_info.major != 2:

    from etc.toolbox import ChoicesEnumMixin, get_choices

    from enum import Enum, unique

    @unique
    class Role(ChoicesEnumMixin, Enum):

        APPLICANT = 0, 'Applicant', 'Description'
        ADMIN = 1, 'Administrator'
        MEMBER = 2

    class Variant(ChoicesEnumMixin, Enum):

        A = 'a'
        B = 'b'

    class MyChoiceModel(models.Model):

        role = models.PositiveIntegerField(
            'Role', choices=get_choices(Role), default=Role.MEMBER)

        variant = models.CharField(
            choices=get_choices(Variant), default=Variant.A, max_length='2')


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
