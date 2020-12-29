Tools for Django Admin
======================


CustomModelPage
---------------

**etc.admin.CustomModelPage** allows easy construction of custom admin pages based on user input.

Use it if you need to perform some action in admin requiring user input.

.. code-block:: python

    from etc.admin import CustomModelPage

    class MyPage(CustomModelPage):

        title = 'Test page 1'  # set page title

        # Define some fields.
        my_field = models.CharField('some title', max_length=10)

        def save(self):
            ...  # Implement data handling.
            super().save()

    # Register my page within Django admin.
    MyPage.register()

