from os import environ
from sys import version_info

import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator
from django.template.base import TemplateSyntaxError

from etc import sites
from etc.sites import DomainGetter
from etc.templatetags.gravatar import gravatar_get_url, gravatar_get_img
from etc.templatetags.model_meta import model_meta_verbose_name, model_meta_verbose_name_plural
from etc.toolbox import set_form_widgets_attrs, choices_list, get_choices, get_site_url, get_model_class_from_string, \
    get_model_class_from_settings, import_app_module, import_project_modules
from tests.testapp.models import MyChildModel1, MyChildModel2, MyChoiceModel, Role, Variant


class MyForm(forms.Form):

    field1 = forms.CharField(label='f1', max_length=100)
    field2 = forms.CharField(label='f2', max_length=100)


class TestInheritedModel:

    def test_texts(self):
        model1 = MyChildModel1()
        fields = {f.name: f for f in model1._meta.fields}
        assert fields['code'].verbose_name == 'Secret code'
        assert fields['expired'].help_text == 'This code is expired.'

        model1 = MyChildModel2()
        fields = {f.name: f for f in model1._meta.fields}
        assert fields['code'].verbose_name == 'Non-secret code'
        assert fields['expired'].help_text == 'dummy'


class TestModelMetaTemplateTags:

    def test_verbose_name_singular(self):
        m = MyChildModel1
        assert model_meta_verbose_name(m) == 'Verb'

    def test_verbose_name_plural(self):
        m = MyChildModel1
        assert model_meta_verbose_name_plural(m) == 'VerbPlural'


class TestModelFieldTemplateTags:

    def test_model_field_x(self, template_render_tag, template_context, settings):

        def check(tag, val, fieldname):

            context = template_context({'model': User()})
            result = template_render_tag('model_field', '%s from %s' % (tag, fieldname), context)
            assert val in result
    
            #
            # `from` missing
            with pytest.raises(TemplateSyntaxError):
                template_render_tag('model_field', '%s %s' % (tag, fieldname))
    
            #
            # `as` clause
            context = template_context({'model': User(), 'field': fieldname.partition('.')[2]})
            result = template_render_tag('model_field', '%s from %s as a' % (tag, fieldname), context)
            assert result == ''
            assert val in context['a']
    
            # field in a variable
            result = template_render_tag('model_field', '%s from model.field' % tag, context)
            assert val in result
    
            #
            # No field at all.
            result = template_render_tag('model_field', '%s from model' % tag, context)
            assert result == ''

            with settings(DEBUG=True):
                with pytest.raises(TemplateSyntaxError):
                    template_render_tag('model_field', '%s from model' % tag, context)

            #
            # Wrong model-field delimiter.
            result = template_render_tag('model_field', '%s from %s' % (tag, fieldname.replace('.', '-')), context)
            assert result == ''
    
            with settings(DEBUG=True):
                with pytest.raises(TemplateSyntaxError):
                    template_render_tag('model_field', '%s from %s' % (tag, fieldname.replace('.', '-')))
    
            #
            # No model in context.
            result = template_render_tag('model_field', '%s from %s' % (tag, fieldname))
            assert result == ''
    
            with settings(DEBUG=True):
                with pytest.raises(TemplateSyntaxError):
                    template_render_tag('model_field', '%s from %s' % (tag, fieldname))
    
            #
            # No field.
            result = template_render_tag('model_field', '%s from model.unknown' % tag, context)
            assert result == ''
    
            with settings(DEBUG=True):
                with pytest.raises(TemplateSyntaxError):
                    template_render_tag('model_field', '%s from model.unknown' % tag, context)

        check('model_field_verbose_name', 'first name', 'model.first_name')
        check('model_field_help_text', 'whether the user can log', 'model.is_staff')

    def test_model_field_homogeneous_sets(self, template_render_tag, template_context):
        # Теги должны принимать не только модель, но и наборы: QuerySet и страницу пагинатора.
        context = template_context({'model': User.objects.all()})
        result = template_render_tag('model_field', 'model_field_verbose_name from model.first_name', context)
        assert 'first name' in result

        page = Paginator(User.objects.all(), 10).page(1)
        context = template_context({'model': page})
        result = template_render_tag('model_field', 'model_field_verbose_name from model.first_name', context)
        assert 'first name' in result


class TestForm:

    def test_set_form_widgets_attrs(self):
        f = MyForm()

        d = {}
        d['class'] = 'clickable'
        d['data-a'] = lambda f: f.__class__.__name__

        set_form_widgets_attrs(f, d)
        output = f.as_p()

        assert output.count('data-a') == 2
        assert output.count('clickable') == 2


class TestGravatarTemplateTags:

    def test_verbose_get_url(self):
        u = User(username='idle')
        url = gravatar_get_url(u, 101, 'retro')
        assert 'http://www.gravatar.com/avatar/ec2f993aec2c27fc750119ab17b16cdb/' in url
        assert 'retro' in url
        assert '101' in url

        u = User(email='idle@sign.som')
        url = gravatar_get_url(u, 101, 'retro')
        assert 'http://www.gravatar.com/avatar/37e24208b31f2a8f1e0f84d4c93fdfb0/' in url
        assert 'retro' in url
        assert '101' in url

        url = gravatar_get_url('idle@sign.som', 101, 'retro')
        assert 'http://www.gravatar.com/avatar/37e24208b31f2a8f1e0f84d4c93fdfb0/' in url
        assert 'retro' in url
        assert '101' in url

        assert gravatar_get_url(None) == ''

    def test_verbose_get_img(self):
        u = User(username='idle')
        url = gravatar_get_img(u, 101, 'retro')
        assert 'http://www.gravatar.com/avatar/ec2f993aec2c27fc750119ab17b16cdb/' in url
        assert 'retro' in url
        assert 'retro' in url
        assert '<img src="' in url

        assert gravatar_get_img(None) == ''


class TestChoices:

    @pytest.mark.skipif(version_info.major == 2, reason='No Enum in Python 2')
    def test_enum(self):

        assert Role.APPLICANT is Role(0)
        assert Role.APPLICANT.value == 0
        assert Role.APPLICANT.title == 'Applicant'
        assert Role.APPLICANT.hint == 'Description'

        assert Role.ADMIN is Role(1)
        assert Role.ADMIN.value == 1
        assert Role.ADMIN.title == 'Administrator'
        assert Role.ADMIN.hint == ''

        assert Role.MEMBER is Role(2)
        assert Role.MEMBER.value == 2
        assert Role.MEMBER.title == 'Member'
        assert Role.MEMBER.hint == ''

        assert Role.get_title(2) == 'Member'
        assert Role.get_title(Role(2)) == 'Member'
        assert Role.get_title(Role.MEMBER) == 'Member'

        assert Role.get_hint(0) == 'Description'
        assert Role.get_hint(Role(0)) == 'Description'
        assert Role.get_hint(Role.APPLICANT) == 'Description'

        assert bool(Role.ADMIN) is True
        assert str(Role.APPLICANT) == '0'
        assert str(Variant.B) == 'b'
        assert int(Role.MEMBER) == 2

        objects = MyChoiceModel.objects

        obj_1 = objects.create()
        obj_2 = objects.create(role=Role.ADMIN, variant=Variant.B)

        assert obj_1.role is Role.MEMBER
        assert obj_1.variant is Variant.A

        assert obj_1.id == objects.get(role=Role.MEMBER).id
        assert obj_2.id == objects.get(variant=Variant.B).id

    def test_enum_db_storage(self):
        # При сохранении члена перечисления в БД должно попадать значение, а не его имя.
        obj = MyChoiceModel.objects.create(role=Role.ADMIN, variant=Variant.B)
        obj.refresh_from_db()

        assert obj.role == 1
        assert obj.variant == 'b'

    def test_choices(self):

        types_dict = choices_list(
            (1, 'T1'),
            (2, 'T2'),
        )

        assert len(types_dict) == 2
        assert types_dict[1] == 'T1'
        assert types_dict[2] == 'T2'

        assert list(types_dict.keys()) == [1, 2]

        ch = get_choices(types_dict)
        assert len(ch) == 2

        assert ch[0][0] == 1
        assert ch[0][1] == 'T1'

        assert ch[1][0] == 2
        assert ch[1][1] == 'T2'


class TestGetModelClass:

    def test_from_settings(self):
        attr_name = 'some'
        fake_settings = type('fake', (object,), {attr_name: 'auth.User'})

        assert get_model_class_from_settings(fake_settings, attr_name) is User

    def test_from_string(self):
        cl = get_model_class_from_string('auth.User')
        assert cl is User

        with pytest.raises(ImproperlyConfigured):
            get_model_class_from_string('some')

        with pytest.raises(ImproperlyConfigured):
            get_model_class_from_string('etc.InheritedModel')


class TestGetSiteUrl:

    def test_basic(self, settings):
        assert get_site_url() == 'http://example.com'

        with settings(SITE_PROTO='htt'):
            assert get_site_url() == 'htt://example.com'
            environ['SITE_PROTO'] = 'ttp'
            assert get_site_url() == 'ttp://example.com'

        environ['SITE_PROTO'] = 'https'
        assert get_site_url() == 'https://example.com'

        environ['SITE_SCHEME'] = 'ftp'
        assert get_site_url() == 'https://example.com'

        del environ['SITE_PROTO']
        assert get_site_url() == 'ftp://example.com'

        environ['SITE_URL'] = 'http://pythonz.net'
        assert get_site_url() == 'http://pythonz.net'

        environ['SITE_DOMAIN'] = 'mydomain.loc'
        assert get_site_url() == 'ftp://mydomain.loc'

        environ['SITE_URL'] = 'http://pythonz.net'
        assert get_site_url() == 'ftp://mydomain.loc'

        del environ['SITE_DOMAIN']
        del environ['SITE_URL']
        del environ['SITE_SCHEME']

        class FakeRequest:

            scheme = 'xyz'

            @classmethod
            def get_host(cls):
                return 'fake'

        assert get_site_url(request=FakeRequest) == 'xyz://example.com'

    def test_tempalte_tag(self, template_render_tag):
        url = 'http://pythonz.net'

        environ['SITE_URL'] = url
        result = template_render_tag('etc_misc', 'site_url')
        assert result == url

    def test_domain_getter(self):
        assert DomainGetter('fake').get_host() == 'fake'
        assert DomainGetter(None).get_host() is None

    def test_fallbacks(self, monkeypatch, settings):
        for var in ('SITE_URL', 'SITE_DOMAIN', 'SITE_PROTO', 'SITE_SCHEME'):
            monkeypatch.delenv(var, raising=False)

        monkeypatch.setattr(sites, 'get_current_site', lambda request: DomainGetter(None))

        with settings(SITE_URL=None, SITE_DOMAIN=None):
            assert get_site_url() == 'http://undefined-domain.local'


class TestImportModules:

    def test_import_app_module(self):
        m = import_app_module('etc', 'sites')
        assert hasattr(m, 'DomainGetter')

        with pytest.raises(ImportError):
            import_app_module('unknown', 'uknown')

        m = import_app_module('etc', 'uknown')
        assert m is None

    def test_import_app_module_bubbles_import_error(self):
        # Ошибка импорта внутри существующего подмодуля не должна замалчиваться.
        with pytest.raises(ImportError, match='Simulated broken module'):
            import_app_module('tests.testapp', 'brokenmod')

        m = import_app_module('django.contrib.admin.apps.SimpleAdminConfig', '__init__')
        assert hasattr(m, 'site')

    def test_import_project_modules(self):
        m = import_project_modules('toolbox')

        assert len(m) == 1
        assert hasattr(m[0], 'get_site_url')


def test_include_formatted(request_client):
    result = request_client().get('/index/')
    assert result.content == b'\n<body>thisone\nstatic\n<sub>dynamic</sub>\ndefault\n</body>'


def test_include_formatted_isolated(template_render_tag):
    result = template_render_tag('etc_misc', 'include_ "sub_{{ postfix }}.html" only', {'postfix': 'static'})
    assert 'static' in result


class TestMiscFilters:

    def test_from(self):
        from django.template import Context, Template

        out = Template('{% load etc_misc %}{{ "k"|from:container }}').render(Context({"container": {"k": "v"}}))
        assert out == "v"

        out = Template('{% load etc_misc %}{{ "x"|from:container }}').render(Context({"container": {"k": "v"}}))
        assert out == "None"

    def test_split(self):
        from django.template import Context, Template

        out = Template('{% load etc_misc %}{{ value|split:","|join:"|" }}').render(Context({"value": "a,b,c"}))
        assert out == "a|b|c"


class TestStaticvTag:

    def test_tag(self, template_render_tag):
        from etc.templatetags import etc_misc

        result = template_render_tag("etc_misc", 'staticv "js/some.js"')
        assert result == f"/static/js/some.js?v={etc_misc.STATIC_VERSION}"

    def test_version_from_settings(self, settings):
        from importlib import reload

        from etc.templatetags import etc_misc

        with settings(STATIC_VERSION=42):
            assert reload(etc_misc).STATIC_VERSION == 42

        reload(etc_misc)
