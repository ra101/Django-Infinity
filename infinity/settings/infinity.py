from decouple import config

from .essentials import Settings as EssentialSettings


class Settings(EssentialSettings):

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = config("DEBUG", cast=bool, default=True)

    INSTALLED_APPS = EssentialSettings.INSTALLED_APPS + ["drf_yasg"]
