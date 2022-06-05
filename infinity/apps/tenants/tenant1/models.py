from django.db import models


class ExampleForTenant1(models.Model):
    """
    Abstract model to maintain architecture of DRF
    """

    data = models.JSONField(default=dict)
