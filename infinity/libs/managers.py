from django.contrib.gis.db.models import Manager
from timescale.db.models.managers import TimescaleManager

from .querysets import GhostQuerySet
from timescale.db.models.querysets import TimescaleQuerySet


class GhostManager(Manager):
    """
    Manager for GhostModel
    """

    def get_queryset(self):
        """
        Get all `non-ghosted` objects.
        """
        return GhostQuerySet(self.model, using=self._db).filter(alive=True)

    def annihilate(self):
        """
        Permanently delete all the objects.
        """
        return GhostQuerySet(self.model, using=self._db).annihilate()

    def resurrect(self):
        """
        Restore all the `ghost`-ed objects.
        """
        return GhostQuerySet(self.model, using=self._db).resurrect()


class TimeScaleManager(TimescaleManager):
    """
    Renaming it, 'cuz ... I want too :p
    """

    pass


class InfiniteManager(GhostManager, TimeScaleManager):
    """
    Manager for InfiniteModel
    """

    def get_queryset(self):
        """
        Get all `non-ghosted` objects, time based objects
        """
        return TimescaleQuerySet(self.model, using=self._db).filter(alive=True)
