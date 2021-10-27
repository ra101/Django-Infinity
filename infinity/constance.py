from .constants import LiveDemoInitialConfig


class LiveSettingsMixin:
    """
    Mixin for all the Constance(Live Setting) Variables
    """

    CONSTANCE_BACKEND = "constance.backends.memory.MemoryBackend"
    CONSTANCE_DATABASE_CACHE_BACKEND = "default"

    CONSTANCE_CONFIG = {
        "LIVE_KEY": (
            LiveDemoInitialConfig.KEY,
            LiveDemoInitialConfig.KEY_HELP,
            str,
        ),
        "LIVE_VALUE": (
            LiveDemoInitialConfig.VALUE,
            LiveDemoInitialConfig.VALUE_HELP,
            str,
        ),
        "LIVE_URL_ENDPOINT": (
            LiveDemoInitialConfig.ENDPOINT,
            LiveDemoInitialConfig.ENDPOINT_HELP,
            str,
        ),
    }

    CONSTANCE_CONFIG_FIELDSETS = {
        "Response": {"fields": ("LIVE_KEY", "LIVE_VALUE"), "collapse": True},
        "URL": ("LIVE_URL_ENDPOINT",),
    }
