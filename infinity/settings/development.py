from .essentials import Settings as EssentialSettings


class Settings(EssentialSettings):
    DEBUG = True
    INSTALLED_APPS = EssentialSettings.INSTALLED_APPS + ["drf_yasg"]
    SHOW_TOOLBAR_CALLBACK = lambda _: DEBUG
