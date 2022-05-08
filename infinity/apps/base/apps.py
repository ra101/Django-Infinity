from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = "apps.base"

    def ready(self):
        from . import signals
