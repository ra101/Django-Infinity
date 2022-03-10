from django.urls import path

from .views import live_view, version_view


urlpatterns = [
    path("version/", version_view),
    path("live_settings/<str:live_url_endpoint>/", live_view, name="live-url-demo"),
]
