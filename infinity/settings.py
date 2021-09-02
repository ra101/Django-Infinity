import os
from sys import path

from configurations import Configuration


class Settings(Configuration):
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    path.append(PROJECT_ROOT)

    BASE_DIR = os.path.dirname(PROJECT_ROOT)

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "django-insecure-ig78b7gll!99blz%d12v-(hbjwktpvk6o@no655e8$#zyaluy2"

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = ["*"]

    # Application definition

    DJANGO_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]

    # THIRD_PARTY_APPS
    EXTENSION_APPS = [
        "rest_framework",
        "drf_yasg",
    ]

    LOCAL_APPS = [
        "apps.base.apps.BaseConfig",
    ]

    INSTALLED_APPS = (
        ["whitenoise.runserver_nostatic"] + DJANGO_APPS + EXTENSION_APPS + LOCAL_APPS
    )

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        # WhiteNoise Middleware above all else other than security
        "libs.staticfiles.middleware.ExtendedWhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
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

    WSGI_APPLICATION = "infinity.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/3.2/ref/settings/#databases

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": f"{BASE_DIR}/db.sqlite3",
        }
    }

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

    STATIC_URL = "/static/"
    STATIC_ROOT = f"{BASE_DIR}/staticfiles/"
    # Multi deploy platform support
    OTHER_STATIC_ROOTS = [
        f"{PROJECT_ROOT}/staticfiles/",
        f"infinity/{BASE_DIR}/staticfiles/",
    ]
    STATICFILES_STORAGE = "libs.staticfiles.storage.ExtendedWhiteNoiseStorage"
    WHITENOISE_MANIFEST_STRICT = False

    # Default primary key field type
    # https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    # Default appending of `/` in URLs
    # https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-APPEND_SLASH

    APPEND_SLASH = True
