Tools for Django Admin
======================


CustomModelPage
---------------

**etc.admin.CustomModelPage** allows easy construction of custom admin pages processing user input.

Use it if you need to perform some action in admin requiring user input.

.. code-block:: python

    from etc.admin import CustomModelPage

    class MyPage(CustomModelPage):

        title = 'Test page 1'  # set page title

        # Define some fields.
        my_field = models.CharField('some title', max_length=10)

        def save(self):
            ...  # Implement data handling from self attributes here.
            
            # self.bound_admin has some useful methods.
            # self.bound_request allows you to access current HTTP request.
            self.bound_admin.message_success(self.bound_request, f'Hey, done!')
            
            super().save()

    # Register my page within Django admin.
    MyPage.register()

