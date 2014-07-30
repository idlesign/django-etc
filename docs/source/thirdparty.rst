Thirdparty Related Bits
=======================


`gravatar` Template Tags
------------------------

* **gravatar_get_url** tag.

    Returns Gravatar image URL for a given string or UserModel.

    Accepts ``size`` integer and ``default`` image identifier as a string

    (see http://ru.gravatar.com/site/implement/images/#default-image).

    .. code-block:: html

        {% load gravatar %}
        {% gravatar_get_url user_model %}


* **gravatar_get_img** tag.

    Returns Gravatar image HTML tag for a given string or UserModel.

    Accepts ``size`` integer and ``default`` image identifier as a string

    (see http://ru.gravatar.com/site/implement/images/#default-image).

    .. code-block:: html

        {% load gravatar %}
        {% gravatar_get_img user_model %}

