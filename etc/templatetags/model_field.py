from django import template
from django.conf import settings


register = template.Library()


@register.tag
def model_field_verbose_name(parser, token):
    """Returns model field verbose name.
    Two notations are acceptable:

        1. Two arguments:
           {% model_field_verbose_name from myfield %}

           Is used to render verbose name of `myfield`.

        2. Four arguments:
           {% model_field_verbose_name from myfield as myvar %}

           Is used to put `myfield` verbose name into `myvar` template variable.

    """
    return _get_model_field_attr('model_field_verbose_name', 'verbose_name', token)


@register.tag
def model_field_help_text(parser, token):
    """Returns model field help text.
    Two notations are acceptable:

        1. Two arguments:
           {% model_field_help_text from myfield %}

           Is used to render verbose name of `myfield`.

        2. Four arguments:
           {% model_field_help_text from myfield as myvar %}

           Is used to put `myfield` verbose name into `myvar` template variable.

    """
    return _get_model_field_attr('model_field_help_text', 'help_text', token)


def _get_model_field_attr(tag_name, attr_name, token):
    tokens = token.split_contents()
    tokens_num = len(tokens)

    if tokens_num not in (3, 5):
        raise template.TemplateSyntaxError('`%(tag_name)s` tag requires two or four arguments. '
                                           'E.g.: {%% %(tag_name)s myfield %%} '
                                           'or {%% %(tag_name)s myfield as myvar %%}.' % {'tag_name': tag_name})

    field = tokens[2]
    as_var = None

    tokens = tokens[3:]
    if len(tokens) >= 2 and tokens[-2] == 'as':
        as_var = tokens[-1]

    return FieldAttrNode(field, attr_name, tag_name, as_var)


class FieldAttrNode(template.Node):

    def __init__(self, field, attr_name, tag_name, as_var=None):
        self.tag_name = tag_name
        self.field = field
        self.attr_name = attr_name
        self.as_var = as_var

    def render(self, context):
        as_var = self.as_var

        def return_contents(contents):
            if as_var is not None:
                context[as_var] = contents
                return ''
            return contents

        var_field = template.Variable(self.field)
        var_model = var_field.lookups[0]

        try:
            field_name = var_field.lookups[1]
        except IndexError:
            if settings.DEBUG:
                raise template.TemplateSyntaxError('`%s` template tag requires model.field notation '
                                                   'but `%s` is given.' % (self.tag_name, self.field))
            return return_contents('')

        try:
            model = template.Variable(var_model).resolve(context)
        except template.VariableDoesNotExist:
            if settings.DEBUG:
                raise template.TemplateSyntaxError('`%s` template tag error: `%s` model '
                                                   'is not found in context.' % (self.tag_name, var_model))
            return return_contents('')

        fields_name_map = model._meta._name_map

        try:
            model_field = fields_name_map[field_name][0]
            contents = getattr(model_field, self.attr_name)
        except KeyError:
            contents = ''
            if settings.DEBUG:
                raise template.TemplateSyntaxError('`%s` template tag error: `%s` field is not found in `%s` model. '
                                                   'Possible choices: %s.' % (self.tag_name,
                                                                              field_name, model.__class__.__name__,
                                                                              ', '.join(fields_name_map.keys())))
        return return_contents(contents)
