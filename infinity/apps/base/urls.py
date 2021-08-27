from django.urls import path

from .views import hello_world, readme


urlpatterns = [
    path("home.html", hello_world, name="base"),
    path("", readme, name="base"),
]
