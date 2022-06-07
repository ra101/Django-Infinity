from django.db import models


class ExampleForTenant1(models.Model):
    """
    Abstract model to maintain architecture of DRF
    """

    data = models.JSONField(default=dict)

    class Meta:
        """
        Meta for ExampleForTenant1
        """

        verbose_name_plural = verbose_name = 'Example Model for Tenant 1'
