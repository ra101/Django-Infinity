from whitenoise.storage import CompressedManifestStaticFilesStorage


class ExtendedWhiteNoiseStorage(CompressedManifestStaticFilesStorage):
    """Handles any issue created by WhiteNoise Storage"""

    def hashed_name(self, name, content=None, filename=None):
        """
        hashed_name raises ValueError if any certain file does not exists or, not found
        we catch this error and reutrns the original name (any name would have worked)
        to make sure even if the staticfiles.json is not found, it does not cause any error
        """
        try:
            return super().hashed_name(name, content, filename)
        except ValueError:
            return name
