from typing import Union, Set, List, Tuple, Dict, Type, Any


class ChoicesEnumMixin:
    """Mixin to add to your enum classes.
    Allows custom titles and hint for enum elements.

    An enum with this mixin has:
        * titles
        * hints

    Every enum item has:
        * title
        * hint

    To be used in conjunction with `get_choices()`.

    .. code-block:: python

        from enum import Enum, unique

        @unique
        class Role(ChoicesEnumMixin, Enum):

            APPLICANT = 0, 'Title', 'Hint'
            ADMIN = 1, 'Administrator'
            MEMBER = 2

        class MyChoiceModel(models.Model):

            role = models.PositiveIntegerField(
                choices=get_choices(Role), default=Role.MEMBER)

        members = MyChoiceModel.objects.filter(role=Role.MEMBER)

    """
    titles = None
    """Value to title mapping."""

    hints = None
    """Value to hint mapping."""

    def __init__(self, *args):
        # Members are declared either with a bare value or a (value, title, hint) tuple.
        # Enum machinery stores the whole declaration tuple in _value_, so we narrow it
        # down to the bare value here. __new__ is deliberately not defined in this mixin:
        # otherwise enum treats the mixin as a data type and replaces __str__ with its own.
        if isinstance(self._value_, tuple):
            self._value_ = args[0]

        cls = self.__class__
        value = self.value

        title = args[1] if len(args) > 1 else None
        hint = args[2] if len(args) > 2 else ''

        if title is None:
            title = self.name.lower().capitalize()

        self.title = title
        self.hint = hint

        def contribute_to_mapping(name, val):

            mapping = getattr(cls, name, None)

            if mapping is None:
                mapping = {}
                setattr(cls, name, mapping)

            mapping[value] = val

        contribute_to_mapping('titles', title)
        contribute_to_mapping('hints', hint)

    @classmethod
    def _missing_(cls, value):
        # The enum reverse lookup map is keyed by declaration tuples,
        # so we search for a member by its bare value.
        for member in cls._member_map_.values():
            if member._value_ == value:
                return member

        return None

    def __bool__(self):
        # Try to be compatible with boolean fields and lookups.
        return bool(self.value)

    def __str__(self):
        # Try to be compatible with text fields and lookups.
        return str(self.value)

    def __int__(self):
        # Try to be compatible with integer fields and lookups.
        return int(self.value)

    @classmethod
    def get_title(cls, item) -> str:
        """Returns a title for a variant instance or it's value.

        :param item:

        """
        if isinstance(item, cls):
            return item.title

        return cls.titles[item]

    @classmethod
    def get_hint(cls, item) -> str:
        """Returns a hint for a variant instance or it's value.

        :param item:

        """
        if isinstance(item, cls):
            return item.hint

        return cls.hints[item]


def choices_list(*choices: Union[Set, List, Tuple, Dict]) -> dict:
    """Helps to define choices for models, that could be addressed
    later as dictionaries.

    To be used in conjunction with `get_choices()`.

    Returns choices ordered dictionary.

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

    :param choices:

    """
    return dict(choices)


def get_choices(choices_list: Union[Dict, Type[ChoicesEnumMixin]]) -> Tuple[Tuple[Any, Any], ...]:
    """Returns model field choices from a given choices list.

    :param  choices_list:
        The list can be defined with `choices_list()` or could be an `ChoicesEnumMixin` and `Enum` subclass.

    """
    if isinstance(choices_list, type) and issubclass(choices_list, ChoicesEnumMixin):
        return tuple(choices_list.titles.items())

    return tuple((key, val) for key, val in choices_list.items())
