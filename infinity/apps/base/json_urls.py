from django.urls import path

from .views import live_view


urlpatterns = [
    path("live_settings/<str:live_url_endpoint>/", live_view, name="live-url-demo"),
]
