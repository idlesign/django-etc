from .choices import choices_list, get_choices
from .importing import import_app_module, import_project_modules
from .models import get_model_class_from_settings, get_model_class_from_string, InheritedModel
from .sites import get_site_url


def set_form_widgets_attrs(form, attrs):
    """Applies a given HTML attributes to each field widget of a given form.

    Example:

        set_form_widgets_attrs(my_form, {'class': 'clickable'})

    """
    for _, field in form.fields.items():
        attrs_ = dict(attrs)
        for name, val in attrs.items():
            if hasattr(val, '__call__'):
                attrs_[name] = val(field)
        field.widget.attrs = field.widget.build_attrs(attrs_)
