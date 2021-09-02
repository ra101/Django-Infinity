from django.urls import path

from .views import hello_world_view, readme_view


urlpatterns = [
    path("home.html", hello_world_view, name="home"),
    path("", readme_view, name="readme"),
]
