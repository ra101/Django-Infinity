from decouple import config

from .essentials import Settings as EssentialSettings



class Settings(EssentialSettings):
    PROJECT_ROOT = EssentialSettings.PROJECT_ROOT
    BASE_DIR = EssentialSettings.BASE_DIR

    DEBUG = config("DEBUG", cast=bool, default=True)
    SHOW_TOOLBAR_CALLBACK = lambda _: DEBUG

    REDISBOARD_DECODER_CLASS="redisboard.data.UTF8BackslashReplaceDecoder"
    REDISBOARD_SOCKET_CONNECT_TIMEOUT=5
    REDISBOARD_SOCKET_TIMEOUT=5
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        },
    }
    SESSION_ENGINE='django.contrib.sessions.backends.cached_db'
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'redisboard.cli.RedisboardAdminConfig',
        'redisboard',
    )
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    ROOT_URLCONF= "infinity.redis_board_urls"
    ALLOWED_HOSTS=['*']
    LOGGING={
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s | %(name)s - %(message)s',
                'datefmt': '%d/%b/%Y %H:%M:%S',
            }
        },
        'handlers': {
            'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler', 'formatter': 'default'},
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            '': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        },
    }
