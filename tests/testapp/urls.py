from django.contrib import admin
from django.urls import path

from pytest_djangoapp.compat import get_urlpatterns

from .views import index


urlpatterns = get_urlpatterns([
    path('index/', index, name='index'),
    path('admin/', admin.site.urls),
])
