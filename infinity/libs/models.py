import uuid

from django.contrib.gis.db import models
from timescale.db.models.fields import TimescaleDateTimeField

from . import managers


class TimeStampModel(models.Model):
    """
    Keeps a record of created and last-updated date-time
     - Uses TimescaleDB for extensive Queryset
    """

    created_on = TimescaleDateTimeField(auto_now_add=True, interval="1 day")
    updated_on = TimescaleDateTimeField(auto_now=True, interval="1 day")

    timescale = managers.TimeScaleManager()

    class Meta:
        """
        Meta class for TimeStampModel
        """

        abstract = True


class GhostModel(models.Model):
    """
    AfterLife for removed records.
     - Once deleted from here, Soul itself gets detroyed!
    """

    alive = models.BooleanField(default=True, editable=False)

    objects = managers.GhostManager()
    all_objects = models.Manager()

    def delete(self, *args, **kwargs):
        """
        Method to `ghost` an object.
        """

        models.signals.pre_delete.send(sender=self.__class__, instance=self)

        # Don't use .save() otherwise it will trigger save signals
        self.__class__.all_objects.filter(id=self.id).update(alive=False)

        models.signals.post_delete.send(sender=self.__class__, instance=self)

    def resurrect(self):
        """
        Restore `ghost`-ed objects.
        """

        self.__class__.all_objects.filter(id=self.id).update(alive=True)

    def annihilate(self, using=None):
        """
        Permanently delete the objects.
        """

        return super().delete(using)

    class Meta:
        """
        Meta class for GhostModel
        """

        abstract = True


class InfiniteModel(TimeStampModel, GhostModel):
    """
    Inhereted from TimeStamp and GhostModel
     - fields: `id:uuid`, `updated_at`, `created_at`, `alive`
     - managers: `objects`, `timescale`, `all_objects`
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    objects = managers.InfiniteManager()
    all_objects = managers.TimeScaleManager()

    class Meta(TimeStampModel.Meta, GhostModel.Meta):
        """
        Meta class for InfiniteModel
        """

        abstract = True
