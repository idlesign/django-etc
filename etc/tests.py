from django import forms
from django.utils import unittest
from django.db import models
from django.contrib.auth.models import User

from .models import InheritedModel
from .templatetags.model_meta import model_meta_verbose_name, model_meta_verbose_name_plural
from .templatetags.gravatar import gravatar_get_url, gravatar_get_img
from .toolbox import set_form_widgets_attrs, choices_list, get_choices


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


class InheritedModelTest(unittest.TestCase):

    def test_texts(self):
        model1 = MyChildModel1()
        fields = {f.name: f for f in model1._meta.fields}
        self.assertEqual(fields['code'].verbose_name, 'Secret code')
        self.assertEqual(fields['expired'].help_text, 'This code is expired.')

        model1 = MyChildModel2()
        fields = {f.name: f for f in model1._meta.fields}
        self.assertEqual(fields['code'].verbose_name, 'Non-secret code')
        self.assertEqual(fields['expired'].help_text, 'dummy')


class ModelMetaTemplateTagsTest(unittest.TestCase):

    def test_verbose_name_singular(self):
        m = MyChildModel1
        self.assertEqual(model_meta_verbose_name(m), 'Verb')

    def test_verbose_name_plural(self):
        m = MyChildModel1
        self.assertEqual(model_meta_verbose_name_plural(m), 'VerbPlural')


class FormTest(unittest.TestCase):

    def test_set_form_widgets_attrs(self):
        f = MyForm()
        set_form_widgets_attrs(f, {'class': 'clickable'})
        output = f.as_p()
        self.assertIn('id_field1">f1:</label> <input class="clickable', output)
        self.assertIn('id_field2">f2:</label> <input class="clickable', output)


class GravatarTemplateTagsTest(unittest.TestCase):

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

    def test_verbose_get_img(self):
        u = User(username='idle')
        url = gravatar_get_img(u, 101, 'retro')
        self.assertIn('http://www.gravatar.com/avatar/ec2f993aec2c27fc750119ab17b16cdb/', url)
        self.assertIn('retro', url)
        self.assertIn('retro', url)
        self.assertIn('<img src="', url)


class ChoicesTest(unittest.TestCase):

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

