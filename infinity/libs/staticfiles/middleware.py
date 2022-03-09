from django.conf import settings

from whitenoise.middleware import WhiteNoiseMiddleware
from whitenoise.string_utils import decode_if_byte_string


class ExtendedWhiteNoiseMiddleware(WhiteNoiseMiddleware):
    """Handles any issue created by WhiteNoise Middleware"""

    def __init__(self, *args, **kwargs):
        """
        - add file from settings.OTHER_STATIC_ROOTS
        """
        super().__init__(*args, **kwargs)

        if self.other_static_roots:
            for root in self.other_static_roots:
                self.add_files(root, prefix=self.static_prefix)

    def configure_from_settings(self, *args, **kwargs):
        """save settings.OTHER_STATIC_ROOTS to internal value"""
        super().configure_from_settings(*args, **kwargs)

        self.other_static_roots = [
            decode_if_byte_string(root) for root in getattr(settings, 'OTHER_STATIC_ROOTS', [])
        ]
