from django.conf.urls import url
from pytest_djangoapp.compat import get_urlpatterns

from .views import index


urlpatterns = get_urlpatterns([
    url(r'^index/$', index, name='index'),
])
