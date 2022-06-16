from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage


urlpatterns = [
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('redisboard/favicon.ico'), permanent=True)
    ),
    path('', admin.site.urls),
]
