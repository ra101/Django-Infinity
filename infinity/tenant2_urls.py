from django.urls import include, path

from .urls import urlpatterns


urlpatterns = [
    path("", include("apps.tenants.urls")),
    path("", include("apps.tenants.tenant2.urls")),
] + urlpatterns
