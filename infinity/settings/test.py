from .essentials import Settings as BaseSettings


class Settings(BaseSettings):
    DEBUG = True
    ALLOWED_HOSTS = []
    PSQL_DEFAULT = "postgres_default"
    CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
