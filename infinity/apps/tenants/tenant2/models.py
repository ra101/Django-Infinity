from django.db import models


class ModelForTenant2(models.Model):
    """
    Abstract model to maintain architecture of DRF
    """

    data = models.JSONField(default=dict)

    class Meta:
        """
        Meta for ExampleForTenant2
        """

        verbose_name_plural = verbose_name = 'Example Model for Tenant 2'
