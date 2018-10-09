from functools import partial

from django import VERSION
from django import template
from django.template import TemplateDoesNotExist
from django.template.base import UNKNOWN_SOURCE, Lexer, Parser
from django.template.loader_tags import do_include, IncludeNode

try:
    from django.template.loader_tags import construct_relative_path

    # To prevent AttributeError: 'Parser' object has no attribute 'origin'
    def construct_relative_path_(parser, name):
        return construct_relative_path(parser.origin.template_name, name)

except ImportError:
    construct_relative_path_ = lambda parser, name: name  # Sorry sub here for now.

from ..toolbox import get_site_url

if VERSION >= (1, 9, 0):
    get_lexer = partial(Lexer)

else:
    get_lexer = partial(Lexer, origin=UNKNOWN_SOURCE)


register = template.Library()


@register.simple_tag(takes_context=True)
def site_url(context):
    """Tries to get a site URL from environment and settings.

    See toolbox.get_site_url() for description.

    Example:

        {% load etc_misc %}
        {% site_url %}

    """
    return get_site_url(request=context.get('request', None))


class DynamicIncludeNode(IncludeNode):

    def __init__(self, *args, **kwargs):
        self.fallback = kwargs.pop('fallback', None)
        super(DynamicIncludeNode, self).__init__(*args, **kwargs)

    if VERSION >= (2, 1, 0):

        def render_(self, tpl_new, context):
            template = self.template

            tpl_old = template.var
            template.var = tpl_new

            try:
                return super(DynamicIncludeNode, self).render(context)

            finally:
                template.var = tpl_old

    else:

        # Now we need to turn on context.template.engine.debug to raise exception
        # as in 2.1+
        def render_(self, tpl_new, context):
            template = self.template

            tpl_old = template.var
            template.var = tpl_new
            debug_old = context.template.engine.debug
            context.template.engine.debug = True

            try:
                return super(DynamicIncludeNode, self).render(context)

            finally:
                template.var = tpl_old
                context.template.engine.debug = debug_old

    def render(self, context):
        render_ = self.render_

        try:
            return render_(
                tpl_new=Parser(get_lexer(self.template.var).tokenize()).parse().render(context),
                context=context)

        except TemplateDoesNotExist:
            fallback = self.fallback

            if not fallback:  # pragma: nocover
                raise

            return render_(tpl_new=fallback.var, context=context)


@register.tag('include_')
def include_(parser, token):
    """Similar to built-in ``include`` template tag, but allowing
    template variables to be used in template name and a fallback template,
    thus making the tag more dynamic.

    .. warning:: Requires Django 1.8+

    Example:

        {% load etc_misc %}
        {% include_ "sub_{{ postfix_var }}.html" fallback "default.html" %}

    """
    bits = token.split_contents()

    dynamic = False

    # We fallback to built-in `include` if a template name contains no variables.
    if len(bits) >= 2:
        dynamic = '{{' in bits[1]

        if dynamic:
            fallback = None
            bits_new = []

            for bit in bits:

                if fallback is True:
                    # This bit is a `fallback` argument.
                    fallback = bit
                    continue

                if bit == 'fallback':
                    fallback = True

                else:
                    bits_new.append(bit)

            if fallback:
                fallback = parser.compile_filter(construct_relative_path_(parser, fallback))

            token.contents = ' '.join(bits_new)

    token.contents = token.contents.replace('include_', 'include')
    include_node = do_include(parser, token)

    if dynamic:
        # swap simple include with dynamic
        include_node = DynamicIncludeNode(
            include_node.template,
            extra_context=include_node.extra_context,
            isolated_context=include_node.isolated_context,
            fallback=fallback or None,
        )

    return include_node
