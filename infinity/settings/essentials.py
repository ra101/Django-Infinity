import os
from sys import path

from decouple import config
from configurations import Configuration
from pendulum import duration

from infinity.__version__ import __version__
from infinity.libs.utils import parse_db_url
from .mixins.constance import LiveSettingsMixin
from .mixins.celery import CelerySettingsMixin


class Settings(CelerySettingsMixin, LiveSettingsMixin, Configuration):
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path.append(PROJECT_ROOT)

    BASE_DIR = os.path.dirname(PROJECT_ROOT)

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = config("SECRET_KEY")
    DEBUG = config("DEBUG", cast=bool, default=True)
    # SHOW_TOOLBAR_CALLBACK = lambda _: DEBUG
    PROJECT_VERSION = __version__

    ALLOWED_HOSTS = ["*"]

    ASGI_APPLICATION = "infinity.asgi.application"

    HAS_MULTI_TYPE_TENANTS = True
    MULTI_TYPE_DATABASE_FIELD = 'schema_name'

    # pre-processing Apps
    PRE_PROCESSING_APPS = [
        "django_tenants",
        # "whitenoise.runserver_nostatic",
        # "adminactions",
        # "libs.infinite_admin",
    ]

    # Core Django Application
    DJANGO_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.gis",
    ]

    # 3rd Party Apps (Shared Schema for each Tenant)
    SHARED_EXTENSION_APPS = [
        "rest_framework",
        "graphene_django",
        "redisboard",
        # "admin_honeypot",
        # "captcha",
        # "django_secure_password_input",
        # "compressor",
        # "django_extensions",
        # "drf_yasg",
        # "debug_toolbar",
    ]

    # 3rd Party Apps (Separate Schema for each Tenant)
    EXTENSION_APPS = [
        "constance",
        "constance.backends.database",
        "django_celery_beat",
        # "django_celery_results",
        "channels",
        "rest_framework_simplejwt",
        # "defender",
    ]

    # Local Apps are generally tenant specific but,
    # We don't care for these being tenant specific,
    # Since it is a mock project.
    SHARED_LOCAL_APPS = [
        "apps.base",
        "apps.infinite_redis",
        "apps.infinite_psql"
    ]

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
            "APPS": TENANT1_APPS, "URLCONF": "infinity.tenant1_urls"
        },
        config('TENANT2_NAME', default='tenant2'): {
            "APPS": TENANT2_APPS, "URLCONF": "infinity.tenant2_urls"
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

        # # Adds Debug Toolbar on response for requests mades and
        # # It is above auth middleware, for bypassing authentication.
        # "debug_toolbar.middleware.DebugToolbarMiddleware",

        # Enables user support (add `user` attribute in <request>).
        "django.contrib.auth.middleware.AuthenticationMiddleware",

        # # Records Failed login attempts for blacklisting.
        # "defender.middleware.FailedLoginMiddleware",

        # Enables cookie- and session-based message support.
        "django.contrib.messages.middleware.MessageMiddleware",

        # Simple clickjacking protection via the X-Frame-Options header.
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "infinity.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    REST_FRAMEWORK = {
        "DEFAULT_PAGINATION_CLASS": "libs.pagination.FormattedPagination",
        "PAGE_SIZE": 10,
        "SEARCH_PARAM": "searchTerm",
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        ],
        "DEFAULT_PERMISSION_CLASSES": [
            "libs.permissions.IsSuperUserOrReadOnly",
        ],
        "DEFAULT_RENDERER_CLASSES": (
            "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        ),
        "DEFAULT_PARSER_CLASSES": (
            "djangorestframework_camel_case.parser.CamelCaseFormParser",
            "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
            "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        ),
        "DEFAULT_THROTTLE_CLASSES": [
            "rest_framework.throttling.AnonRateThrottle",
        ],
        "DEFAULT_THROTTLE_RATES": {"anon": "100/day"},
    }

    SIMPLE_JWT = {
        "ACCESS_TOKEN_LIFETIME": duration(minutes=5),
        "REFRESH_TOKEN_LIFETIME": duration(minutes=20),
    }

    # Redis Setup
    REDIS_URL = config("REDIS_URL", default=None)

    if not REDIS_URL:
        REDIS_URL = (
            f"redis://:{config('REDIS_PASS')}"
            + f"@{config('REDIS_HOST', default='localhost')}"
            + f":{config('REDIS_PORT', cast=int, default=6379)}"
        )

    CELERY_BROKER_URL = REDIS_URL

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
            'KEY_FUNCTION': 'django_tenants.cache.make_key',
            'REVERSE_KEY_FUNCTION': 'django_tenants.cache.reverse_key',
        }
    }

    CHANNEL_LAYERS = {"default": {"CONFIG": {"hosts": [REDIS_URL]}}}

    # PostgreSQL Setup
    PSQL_DEFAULT = "postgres"

    DATABASES = {
        "default": config(
            "PSQL_URL",
            cast=parse_db_url("django_tenants.postgresql_backend"),
            default=(
                f"postgres://{config('PSQL_USER', default=PSQL_DEFAULT)}"
                + f":{config('PSQL_PASS')}"
                + f"@{config('PSQL_HOST', default='localhost')}"
                + f":{config('PQSL_PORT', cast=int, default=5432)}"
                + f"/{config('PSQL_NAME', default=PSQL_DEFAULT)}"
            ),
        )
    }

    # `django_tenants.postgresql_backend` is inherited by `ORIGINAL_BACKEND`
    ORIGINAL_BACKEND = "timescale.db.backends.postgis"

    DATABASE_ROUTERS = [
        'django_tenants.routers.TenantSyncRouter',
    ]

    TENANT_MODEL = "base.Tenant"
    TENANT_DOMAIN_MODEL = "base.Domain"

    GDAL_LIBRARY_PATH = config("GDAL_LIBRARY_PATH")
    GEOS_LIBRARY_PATH = config("GEOS_LIBRARY_PATH")

    # Password validation
    # https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/3.2/topics/i18n/

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # http://whitenoise.evans.io/en/stable/

    STATIC_URL = COMPRESS_URL = "/static/"
    # STATIC_ROOT = COMPRESS_ROOT = f"{BASE_DIR}/infinity/static/"

    # # Multi platform deploy support
    # OTHER_STATIC_ROOTS = [
    #     f"{PROJECT_ROOT}/static/",
    #     f"infinity/{BASE_DIR}/static/",
    # ]
    # STATICFILES_STORAGE = COMPRESS_STORAGE = str(
    #     "libs.staticfiles.storage.ExtendedWhiteNoiseStorage"
    # )
    # WHITENOISE_MANIFEST_STRICT = False

    # Default primary key field type
    # https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
    DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

    # Default appending of `/` in URLs
    # https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-APPEND_SLASH

    APPEND_SLASH = True

    INTERNAL_IPS = ["127.0.0.1"]

    # # Debug Toolbar Setup
    # DEBUG_TOOLBAR_PANELS = [
    #     "debug_toolbar.panels.versions.VersionsPanel",
    #     "debug_toolbar.panels.timer.TimerPanel",
    #     "debug_toolbar.panels.settings.SettingsPanel",
    #     "debug_toolbar.panels.headers.HeadersPanel",
    #     "debug_toolbar.panels.request.RequestPanel",
    #     "debug_toolbar.panels.sql.SQLPanel",
    #     "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    #     "debug_toolbar.panels.templates.TemplatesPanel",
    #     "debug_toolbar.panels.cache.CachePanel",
    #     "debug_toolbar.panels.signals.SignalsPanel",
    #     "debug_toolbar.panels.logging.LoggingPanel",
    #     "debug_toolbar.panels.redirects.RedirectsPanel",
    # ]

    # DEBUG_TOOLBAR_CONFIG = {
    #     "INTERCEPT_REDIRECTS": False,
    # }
