from django.db import models

from apps.redis_db_app.manager import RedisModelManager


class RedisAbstractModel(models.Model):
    """
    Abstract model to maintain architecture of DRF
    """

    key = models.BinaryField(max_length=255)
    value = models.BinaryField(max_length=255)

    objects = RedisModelManager()

    class Meta:
        """Meta class for RedisAbstractModel"""

        managed = False  # shutsdown migrations

    def __str__(self):
        """Dictionary"""
        return "{" f"{self.key}: {self.value}" "}"

    def save(self, value):
        """calling Save of Custom Manager"""
        self.__class__.objects.save(self, value)
        self.value = bytes(value, "utf-8")

    def delete(self):
        """calling Delete of Custom Manager"""
        self.__class__.objects.delete(self)
