from os import environ
from collections import OrderedDict

from django import forms, VERSION
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.base import Template, TemplateSyntaxError
from django.template.context import Context

from .models import InheritedModel
from .templatetags.model_meta import model_meta_verbose_name, model_meta_verbose_name_plural
from .templatetags.gravatar import gravatar_get_url, gravatar_get_img
from .toolbox import set_form_widgets_attrs, choices_list, get_choices, get_site_url, get_model_class_from_string, \
    get_model_class_from_settings, import_app_module, import_project_modules


class MyForm(forms.Form):

    field1 = forms.CharField(label='f1', max_length=100)
    field2 = forms.CharField(label='f2', max_length=100)


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


######################################################################################

class EtcTestCase(TestCase):

    @classmethod
    def render(cls, string, context):
        return Template(string).render(Context(context))


class InheritedModelTest(EtcTestCase):

    def test_texts(self):
        model1 = MyChildModel1()
        fields = {f.name: f for f in model1._meta.fields}
        self.assertEqual(fields['code'].verbose_name, 'Secret code')
        self.assertEqual(fields['expired'].help_text, 'This code is expired.')

        model1 = MyChildModel2()
        fields = {f.name: f for f in model1._meta.fields}
        self.assertEqual(fields['code'].verbose_name, 'Non-secret code')
        self.assertEqual(fields['expired'].help_text, 'dummy')


class ModelMetaTemplateTagsTest(EtcTestCase):

    def test_verbose_name_singular(self):
        m = MyChildModel1
        self.assertEqual(model_meta_verbose_name(m), 'Verb')

    def test_verbose_name_plural(self):
        m = MyChildModel1
        self.assertEqual(model_meta_verbose_name_plural(m), 'VerbPlural')


class ModelFieldTemplateTagsTest(EtcTestCase):

    def test_model_field_verbose_name(self):
        result = self.render(
            "{% load model_field %}{% model_field_verbose_name from model.first_name %}",
            {'model': User()}
        )
        self.assertEqual(result, 'first name')

        #
        # `from` missing
        self.assertRaises(
            TemplateSyntaxError,
            self.render,
            "{% load model_field %}{% model_field_verbose_name model.first_name %}", {}
        )

        #
        # `as` clause
        context = {'model': User()}
        result = self.render(
            "{% load model_field %}{% model_field_verbose_name from model.first_name as a %}",
            context
        )
        self.assertEqual(result, '')
        self.assertEqual(context['a'], 'first name')

        #
        # Wrong model-field delimiter.
        result = self.render(
            "{% load model_field %}{% model_field_verbose_name from model-first_name %}",
            context
        )
        self.assertEqual(result, '')

        with self.settings(DEBUG=True):
            self.assertRaises(
                TemplateSyntaxError,
                self.render,
                "{% load model_field %}{% model_field_verbose_name from model-first_name %}", {}
            )

        #
        # No model in context.
        result = self.render(
            "{% load model_field %}{% model_field_verbose_name from model.first_name %}",
            {}
        )
        self.assertEqual(result, '')

        with self.settings(DEBUG=True):
            self.assertRaises(
                TemplateSyntaxError,
                self.render,
                "{% load model_field %}{% model_field_verbose_name from model.first_name %}", {}
            )

        #
        # No field.
        result = self.render(
            "{% load model_field %}{% model_field_verbose_name from model.unknown %}",
            context
        )
        self.assertEqual(result, '')

        with self.settings(DEBUG=True):
            self.assertRaises(
                TemplateSyntaxError,
                self.render,
                "{% load model_field %}{% model_field_verbose_name from model.unknown %}", context
            )

    def test_model_field_help_text(self):
        result = self.render(
            "{% load model_field %}{% model_field_help_text from model.is_staff %}",
            {'model': User()}
        )
        self.assertIn('whether the user can log', result)

        #
        # `from` missing
        self.assertRaises(
            TemplateSyntaxError,
            self.render,
            "{% load model_field %}{% model_field_help_text %}", {}
        )

        #
        # `as` clause
        context = {'model': User()}
        result = self.render(
            "{% load model_field %}{% model_field_help_text from model.is_staff as a %}",
            context
        )
        self.assertEqual(result, '')
        self.assertIn('whether the user can log', context['a'])

        #
        # Wrong model-field delimiter.
        result = self.render(
            "{% load model_field %}{% model_field_help_text from model-is_staff %}",
            context
        )
        self.assertEqual(result, '')

        with self.settings(DEBUG=True):
            self.assertRaises(
                TemplateSyntaxError,
                self.render,
                "{% load model_field %}{% model_field_help_text from model-is_staff %}", {}
            )

        #
        # No model in context.
        result = self.render(
            "{% load model_field %}{% model_field_help_text from model.is_staff %}",
            {}
        )
        self.assertEqual(result, '')

        with self.settings(DEBUG=True):
            self.assertRaises(
                TemplateSyntaxError,
                self.render,
                "{% load model_field %}{% model_field_help_text from model.is_staff %}", {}
            )

        #
        # No field.
        result = self.render(
            "{% load model_field %}{% model_field_help_text from model.unknown %}",
            context
        )
        self.assertEqual(result, '')

        with self.settings(DEBUG=True):
            self.assertRaises(
                TemplateSyntaxError,
                self.render,
                "{% load model_field %}{% model_field_help_text from model.unknown %}", context
            )


class FormTest(EtcTestCase):

    def test_set_form_widgets_attrs(self):
        f = MyForm()
        d = OrderedDict()
        d['class'] = 'clickable'
        d['data-a'] = lambda f: f.__class__.__name__
        set_form_widgets_attrs(f, d)
        output = f.as_p()

        self.assertIn('class="clickable" data-a="CharField" id="id_field1"', output)
        self.assertIn('class="clickable" data-a="CharField" id="id_field2"', output)


class GravatarTemplateTagsTest(EtcTestCase):

    def test_verbose_get_url(self):
        u = User(username='idle')
        url = gravatar_get_url(u, 101, 'retro')
        self.assertIn('http://www.gravatar.com/avatar/ec2f993aec2c27fc750119ab17b16cdb/', url)
        self.assertIn('retro', url)
        self.assertIn('101', url)

        u = User(email='idle@sign.som')
        url = gravatar_get_url(u, 101, 'retro')
        self.assertIn('http://www.gravatar.com/avatar/37e24208b31f2a8f1e0f84d4c93fdfb0/', url)
        self.assertIn('retro', url)
        self.assertIn('101', url)

        url = gravatar_get_url('idle@sign.som', 101, 'retro')
        self.assertIn('http://www.gravatar.com/avatar/37e24208b31f2a8f1e0f84d4c93fdfb0/', url)
        self.assertIn('retro', url)
        self.assertIn('101', url)

        self.assertEqual(gravatar_get_url(None), '')

    def test_verbose_get_img(self):
        u = User(username='idle')
        url = gravatar_get_img(u, 101, 'retro')
        self.assertIn('http://www.gravatar.com/avatar/ec2f993aec2c27fc750119ab17b16cdb/', url)
        self.assertIn('retro', url)
        self.assertIn('retro', url)
        self.assertIn('<img src="', url)

        self.assertEqual(gravatar_get_img(None), '')


class ChoicesTest(EtcTestCase):

    def test_choices(self):

        types_dict = choices_list(
            (1, 'T1'),
            (2, 'T2'),
        )

        self.assertEqual(len(types_dict), 2)
        self.assertEqual(types_dict[1], 'T1')
        self.assertEqual(types_dict[2], 'T2')

        self.assertEqual(list(types_dict.keys()), [1, 2])

        ch = get_choices(types_dict)
        self.assertEqual(len(ch), 2)

        self.assertEqual(ch[0][0], 1)
        self.assertEqual(ch[0][1], 'T1')

        self.assertEqual(ch[1][0], 2)
        self.assertEqual(ch[1][1], 'T2')


class GetModelClassTest(EtcTestCase):

    def test_from_settings(self):
        attr_name = 'some'
        fake_settings = type('fake', (object,), {attr_name: 'auth.User'})

        self.assertIs(get_model_class_from_settings(fake_settings, attr_name), User)

    def test_from_string(self):
        cl = get_model_class_from_string('auth.User')
        self.assertIs(cl, User)

        self.assertRaises(ImproperlyConfigured, get_model_class_from_string, 'some')
        self.assertRaises(ImproperlyConfigured, get_model_class_from_string, 'etc.InheritedModel')


class GetSiteUrlTest(EtcTestCase):

    def test_basic(self):
        self.assertEqual(get_site_url(), 'http://example.com')

        with self.settings(SITE_PROTO='htt'):
            self.assertEqual(get_site_url(), 'htt://example.com')
            environ['SITE_PROTO'] = 'ttp'
            self.assertEqual(get_site_url(), 'ttp://example.com')

        environ['SITE_PROTO'] = 'https'
        self.assertEqual(get_site_url(), 'https://example.com')

        environ['SITE_SCHEME'] = 'ftp'
        self.assertEqual(get_site_url(), 'https://example.com')

        del environ['SITE_PROTO']
        self.assertEqual(get_site_url(), 'ftp://example.com')

        environ['SITE_URL'] = 'http://pythonz.net'
        self.assertEqual(get_site_url(), 'http://pythonz.net')

        environ['SITE_DOMAIN'] = 'mydomain.loc'
        self.assertEqual(get_site_url(), 'ftp://mydomain.loc')

        environ['SITE_URL'] = 'http://pythonz.net'
        self.assertEqual(get_site_url(), 'ftp://mydomain.loc')

        del environ['SITE_DOMAIN']
        del environ['SITE_URL']
        del environ['SITE_SCHEME']

        class FakeRequest(object):

            scheme = 'xyz'

            @classmethod
            def get_host(cls):
                return 'fake'

        self.assertEqual(get_site_url(request=FakeRequest), 'xyz://example.com')

        if VERSION < (1, 7):
            Site._meta.installed = False
            self.assertEqual(get_site_url(), 'http://undefined-domain.local')

    def test_tempalte_tag(self):
        url = 'http://pythonz.net'

        environ['SITE_URL'] = url
        result = self.render('{% load etc_misc %}{% site_url %}', {})
        self.assertEqual(result, url)


class ImportModulesTest(EtcTestCase):

    def test_import_app_module(self):
        m = import_app_module('etc', 'utils')
        self.assertTrue(hasattr(m, 'ModelBase'))

        self.assertRaises(ImportError, import_app_module, 'unknown', 'uknown')

        m = import_app_module('etc', 'uknown')
        self.assertIsNone(m)

        m = import_app_module('django.contrib.admin.apps.SimpleAdminConfig', '__init__')
        self.assertTrue(hasattr(m, 'site'))

    def test_import_project_modules(self):
        m = import_project_modules('toolbox')

        self.assertTrue(len(m) == 1)
        self.assertTrue(hasattr(m[0], 'get_site_url'))

