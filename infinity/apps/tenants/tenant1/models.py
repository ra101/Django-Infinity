from django.db import models


class ModelForTenant1(models.Model):
    """
    Abstract model to maintain architecture of DRF
    """

    data = models.JSONField(default=dict)

    class Meta:
        """
        Meta for ModelForTenant1
        """

        verbose_name_plural = verbose_name = 'Example Model for Tenant 1'
