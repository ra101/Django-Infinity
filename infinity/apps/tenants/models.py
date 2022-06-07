from django.db import models


class ExampleForTenantShared(models.Model):
    """
    Abstract model to maintain architecture of DRF
    """

    data = models.JSONField(default=dict)

    class Meta:
        """
        Meta for ExampleForTenantShared
        """

        verbose_name_plural = verbose_name = 'Example Model for Shared Tenant'
