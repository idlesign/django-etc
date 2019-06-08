from collections import OrderedDict


def choices_list(*choices):
    """Helps to define choices for models, that could be addressed
    later as dictionaries.

    To be used in conjunction with `get_choices()`.

    Example:

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

    :param set|list|tuple choices:
    :rtype: OrderedDict
    :return: Choices ordered dictionary
    """
    return OrderedDict(choices)


def get_choices(choices_list):
    """Returns model field choices from a given choices list.
    Choices list is defined with `choices_list()`.

    :param OrderedDict choices_list:
    :rtype: tuple
    :return: Choices tuple
    """
    return tuple((key, val) for key, val in choices_list.items())
