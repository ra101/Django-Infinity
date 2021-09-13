from django.db import models


class RedisAbstractModel(models.Model):
    """
    Abstract model to maintain architecture of DRF
    """
    key = models.CharField(max_length=255)

    class Meta:
        """Meta class for RedisAbstractModel"""
        managed = False # shutsdown migrations
