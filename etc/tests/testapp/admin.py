from django.db import models

from etc.admin import CustomModelPage, admins


class MyCustomPageModelAdmin(admins.CustomPageModelAdmin):
    """Custom page admin."""
    pass


class MyPage1(CustomModelPage):

    title = 'Test page 1'
    my_field = models.CharField('some title', max_length=10)

    bound_admin = MyCustomPageModelAdmin

    def save(self):
        self.bound_admin.message_warning(self.bound_request, f'test1:{self.my_field}')
        super().save()


class MyPage2(CustomModelPage):

    title = 'Second test page'
    my_another_field = models.TextField('put data here')

    def save(self):
        self.bound_admin.message_error(self.bound_request, f'test2:{self.my_another_field}')


MyPage1.register()
MyPage2.register()
