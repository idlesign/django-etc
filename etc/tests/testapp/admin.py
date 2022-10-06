from django.db import models
from django.http import HttpResponse

from etc.admin import CustomModelPage, admins


class MyCustomPageModelAdmin(admins.CustomPageModelAdmin):
    """Custom page admin."""


class MyPage1(CustomModelPage):

    title = 'Test page 1'
    my_field = models.CharField('some title', max_length=10)

    admin_cls = MyCustomPageModelAdmin

    def save(self):
        self.bound_admin.message_warning(self.bound_request, f'test1:{self.my_field}')
        super().save()


class MyPage2(CustomModelPage):

    title = 'Second test page'
    my_another_field = models.TextField('put data here')

    def save(self):
        val = self.my_another_field
        self.bound_admin.message_error(self.bound_request, f'test2:{val}')

        if val == 'myresponse':
            self.bound_response = HttpResponse(b'fine')


MyPage1.register()
MyPage2.register()
