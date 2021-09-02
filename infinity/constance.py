class LiveSettingsMixin:
    """
    Mixin for all the Constance(Live Setting) Variables
    """

    CONSTANCE_BACKEND = 'constance.backends.memory.MemoryBackend'
    CONSTANCE_DATABASE_CACHE_BACKEND = 'default'


    CONSTANCE_CONFIG = {
        'LIVE_KEY': (
            "Some Random Key",
            "Editable Key for live-setting endpoint",
            str
        ),
        'LIVE_VALUE': (
            "Some Random Value",
            "Editable Value for live-setting endpoint",
            str
        ),
        'LIVE_URL_ENDPOINT': (
            "some_random_url_endpoint",
            "Editable URL Endpoint,"
            "\nTo get the response send a GET Request at "
            "\n/live_settings/<LIVE_URL_ENDPOINT>",
            str
        )
    }

    CONSTANCE_CONFIG_FIELDSETS = {
        'Response': {
            'fields': ('LIVE_KEY', 'LIVE_VALUE'),
            'collapse': True
        },
        'URL': ('LIVE_URL_ENDPOINT',),
    }
