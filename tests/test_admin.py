from django.contrib import admin

from etc.admin import admins

from tests.testapp.admin import MyPage1, MyCustomPageModelAdmin, MyPage2
from tests.testapp.models import MyChildModel2


def test_custom_model_pages(request_client, user_create):
    user = user_create(superuser=True)
    client = request_client(user=user)

    response = client.get('/admin/testapp/')
    assert '/admin/testapp/mypage2/' in response.rendered_content
    assert '/admin/testapp/mypage1/' in response.rendered_content

    response = client.get('/admin/testapp/mypage2/')
    assert 'Put data here' in response.rendered_content

    response = client.post('/admin/testapp/mypage2/', data={'my_another_field': 'hohoho'}, follow=True)
    assert 'Test2:hohoho' in response.rendered_content

    response = client.post('/admin/testapp/mypage2/', data={'my_another_field': 'myresponse'}, follow=True)
    assert response.content == b'fine'

    response = client.post('/admin/testapp/mypage1/', data={'my_field': '1234'}, follow=True)
    assert 'Test1:1234' in response.rendered_content
    assert 'Done.' in response.rendered_content


class TestCustomModelAdminPages:

    def test_custom_model_admin_page(self):

        assert admin.site._registry[MyPage1].__class__ == MyCustomPageModelAdmin

        assert admin.site._registry[MyPage2].__class__ == admins.CustomPageModelAdmin


def test_readonly_admin(admin_client):
    obj = MyChildModel2.objects.create(code='x')

    model_admin = admin.site._registry[MyChildModel2]
    assert model_admin.has_add_permission(None) is False
    assert model_admin.has_delete_permission(None) is False

    admin_client.configure(model=MyChildModel2, app='testapp')
    response = admin_client.call_change(obj)

    assert response.ok
    assert '_save' not in response.text
    assert '_addanother' not in response.text
    assert '_continue' not in response.text
