from django.db import models


class ExampleForTenantShared(models.Model):
    """
    Abstract model to maintain architecture of DRF
    """

    data = models.JSONField(default=dict)
