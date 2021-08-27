from django.urls import path

from .views import hello_world


urlpatterns = [
    path("home.html", hello_world, name="hello_world"),
]
