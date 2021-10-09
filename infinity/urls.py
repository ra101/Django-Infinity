from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from .constants import ProjectDetails


json_urls = [
    path("", include("apps.base.json_urls"), name="base-json"),
    path("", include("apps.infinite_redis.urls")),
]

html_urls = [
    path("", include("apps.base.html_urls"), name="base-html"),
]

schema_view = get_schema_view(
    openapi.Info(
        title=ProjectDetails.TITLE,
        default_version="v1.0.0",
        description=ProjectDetails.DESCRIPTION,
        contact=openapi.Contact(
            name=ProjectDetails.AUTHOR_NAME,
            email=ProjectDetails.AUTHOR_EMAIL,
            url=ProjectDetails.AUTHOR_WEB,
        ),
        license=openapi.License(
            name=ProjectDetails.LICENSE_TYPE, url=ProjectDetails.LICENSE_URL
        ),
    ),
    public=ProjectDetails.IS_PUBLIC,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(json_urls)),
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    # add html url after swagger so, swagger doesn't try to render it
    path("", include(html_urls)),
]
