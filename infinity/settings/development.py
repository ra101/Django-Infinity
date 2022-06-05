from decouple import config

from .essentials import Settings as EssentialSettings



class Settings(EssentialSettings):
    PROJECT_ROOT = EssentialSettings.PROJECT_ROOT
    BASE_DIR = EssentialSettings.BASE_DIR

    DEBUG = True
    SHOW_TOOLBAR_CALLBACK = lambda _: DEBUG

    # pre-processing Apps
    PRE_PROCESSING_APPS = [
        "django_tenants",
        # "whitenoise.runserver_nostatic",
        "adminactions",
        # "libs.infinite_admin",
    ]

    # Core Django Application
    DJANGO_APPS = EssentialSettings.DJANGO_APPS

    # 3rd Party Apps (Shared Schema for each Tenant)
    SHARED_EXTENSION_APPS = [
        "rest_framework",
        "graphene_django",
        # "admin_honeypot",
        # "captcha",
        # "django_secure_password_input",
        # "compressor",
        "drf_yasg",
        "debug_toolbar",
    ]

    # 3rd Party Apps (Separate Schema for each Tenant)
    EXTENSION_APPS = [
        "constance",
        "constance.backends.database",
        "django_celery_beat",
        "django_celery_results",
        "channels",
        "rest_framework_simplejwt",
        # "defender",
    ]

    # Local Apps are generally tenant specific but,
    # We don't care for these being tenant specific,
    # Since it is a mock project.
    SHARED_LOCAL_APPS = EssentialSettings.SHARED_LOCAL_APPS

    PUBLIC_APPS = (
        PRE_PROCESSING_APPS + DJANGO_APPS + SHARED_EXTENSION_APPS \
            + EXTENSION_APPS + SHARED_LOCAL_APPS
    )

    TENANT1_APPS = [
        "apps.tenants",
        "apps.tenants.tenant1",
    ] + EXTENSION_APPS

    TENANT2_APPS = [
        "apps.tenants",
        "apps.tenants.tenant2",
    ] + EXTENSION_APPS

    # Reequired by django-tenants
    TENANT_TYPES = {
        "public": {
            "APPS": PUBLIC_APPS, "URLCONF": "infinity.urls"
        },
        config('TENANT1_NAME', default='tenant1'): {
            "APPS": TENANT1_APPS, "URLCONF": "infinity.urls"
        },
        config('TENANT2_NAME', default='tenant2'): {
            "APPS": TENANT2_APPS, "URLCONF": "infinity.urls"
        },
    }

    # list(dict.fromkeys(<list>)) mantains uniqueness and ordering.
    INSTALLED_APPS = list(dict.fromkeys(
        PUBLIC_APPS + TENANT1_APPS + TENANT2_APPS
    ))

    MIDDLEWARE = [

        # Tenant Middleware is above all, so that each request
        # can be set to use the correct schema.
        "django_tenants.middleware.main.TenantMainMiddleware",

        # Security for request/response cycle.
        "django.middleware.security.SecurityMiddleware",

        # # WhiteNoise Middleware is above all other than security, so that
        # # each request will associated the required template.
        # "libs.staticfiles.middleware.ExtendedWhiteNoiseMiddleware",

        # Enables session support (add `session` attribute in <request>).
        "django.contrib.sessions.middleware.SessionMiddleware",

        # Adds utilities for taking care of basic operations.
        "django.middleware.common.CommonMiddleware",

        # Adds protection against CSRF by adding hidden form fields
        # to POST forms and checking requests for the correct value.
        "django.middleware.csrf.CsrfViewMiddleware",

        # Adds Debug Toolbar on response for requests mades and
        # It is above auth middleware, for bypassing authentication.
        "debug_toolbar.middleware.DebugToolbarMiddleware",

        # Enables user support (add `user` attribute in <request>).
        "django.contrib.auth.middleware.AuthenticationMiddleware",

        # # Records Failed login attempts for blacklisting.
        # "defender.middleware.FailedLoginMiddleware",

        # Enables cookie- and session-based message support.
        "django.contrib.messages.middleware.MessageMiddleware",

        # Simple clickjacking protection via the X-Frame-Options header.
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    # Debug Toolbar Setup
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ]

    DEBUG_TOOLBAR_CONFIG = {
        "INTERCEPT_REDIRECTS": False,
    }
