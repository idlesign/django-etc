from django.db.models.base import ModelBase


class InheritedModelMetaclass(ModelBase):

    def __new__(cls, name, bases, attrs):
        cl = super(InheritedModelMetaclass, cls).__new__(cls, name, bases, attrs)
        texts_marker = '_texts_applied'
        if not getattr(cl, texts_marker, False):
            try:
                names_map = {f.name: f for f in cl._meta.fields}
            except AttributeError:
                return cl
            fields_cl = getattr(cl, 'Fields', None)
            if fields_cl is not None:
                for attr_name, val in fields_cl.__dict__.items():
                    if not attr_name.startswith('_'):
                        if attr_name in names_map:
                            field = names_map[attr_name]
                            if not isinstance(val, dict):
                                val = {'verbose_name': val}
                            for field_attr, field_val in val.items():
                                setattr(field, field_attr, field_val)
            setattr(cl, texts_marker, True)
        return cl


class DomainGetter(object):

    __slots__ = ['domain']

    def __init__(self, domain):
        self.domain = domain

    def get_host(self):
        return self.domain
