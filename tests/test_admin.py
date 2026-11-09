from django.contrib import admin

from etc.admin import admins

from etc.tests.testapp.admin import MyPage1, MyCustomPageModelAdmin, MyPage2


def test_custom_model_pages(request_client, user_create):
    user = user_create(superuser=True)
    client = request_client(user=user)

    response = client.get('/admin/admin/')
    assert '/admin/admin/mypage2/' in response.rendered_content
    assert '/admin/admin/mypage1/' in response.rendered_content

    response = client.get('/admin/admin/mypage2/')
    assert 'Put data here' in response.rendered_content

    response = client.post('/admin/admin/mypage2/', data={'my_another_field': 'hohoho'}, follow=True)
    assert 'Test2:hohoho' in response.rendered_content

    response = client.post('/admin/admin/mypage2/', data={'my_another_field': 'myresponse'}, follow=True)
    assert response.content == b'fine'

    response = client.post('/admin/admin/mypage1/', data={'my_field': '1234'}, follow=True)
    assert 'Test1:1234' in response.rendered_content
    assert 'Done.' in response.rendered_content


class TestCustomModelAdminPages:

    def test_custom_model_admin_page(self):

        assert admin.site._registry[MyPage1].__class__ == MyCustomPageModelAdmin

        assert admin.site._registry[MyPage2].__class__ == admins.CustomPageModelAdmin
