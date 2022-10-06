Tools for Django Admin
======================


CustomModelPage
---------------

**etc.admin.CustomModelPage** allows easy construction of custom admin pages processing user input.

Use it if you need to perform some action in admin requiring user input.

.. code-block:: python

    from django.db import models

    from etc.admin import CustomModelPage, admins
    from etc.tests.testapp.models import MyChildModel1


    class MyPageModelAdmin(admins.CustomPageModelAdmin):

        fields = (
            'my_field', 'moy_relation'
        )
        autocomplete_fields = (
            'my_relation',
        )


    class MyPage(CustomModelPage):

        title = 'Test page 1'  # set page title

        # Define some fields.
        my_field = models.CharField('some title', max_length=10)
        my_relation = models.ForeignKey(MyChildModel1, null=True)

        admin_cls = admins.CustomPageModelAdmin  # set admin class for this page

        def save(self):
            ...  # Implement data handling from self attributes here.

            # self.bound_admin has some useful methods.
            # self.bound_request allows you to access current HTTP request.
            self.bound_admin.message_success(self.bound_request, f'Hey, done!')

            super().save()

            # to return a custom response you can assign self.bound_response
            # this can be useful, e.g. for file downloads
            self.bound_response = HttpResponse(b'%)')


    # Register my page within Django admin.
    MyPage.register()

