from django.urls import path
from constance import config as live_settings

from .views import live_view


urlpatterns = [
    path("live_settings/<str:live_url_endpoint>/", live_view, name="live_url_demo"),
]
