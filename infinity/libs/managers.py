from polymorphic.managers import PolymorphicManager
from psqlextra.manager import PostgresManager as PSQLExtraManager
from timescale.db.models.managers import TimescaleManager

from . import querysets as qs


class SoftDeleteManager(PSQLExtraManager):
    """
    Manager for SoftDeleteModel
    """

    def get_queryset(self):
        """
        Get all `hard-deleted` objects.
        """
        return qs.SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=True)

    def hard_delete(self):
        """
        Permanently delete all the objects.
        """
        return qs.SoftDeleteQuerySet(self.model, using=self._db).hard_delete()

    def restore(self):
        """
        Restore all the `soft-delete`-ed objects.
        """
        return qs.SoftDeleteQuerySet(self.model, using=self._db).restore()


class TimeScaleManager(TimescaleManager, PSQLExtraManager):
    queryset_class = qs.TimeScaleQuerySet

    def get_queryset(self):
        return qs.TimeScaleQuerySet(self.model, using=self._db)


class PolymorphicExtraManager(PolymorphicManager, PSQLExtraManager):

    queryset_class = qs.PolymorphicExtraQuerySet


class InfiniteManager(TimeScaleManager, PolymorphicExtraManager):
    """
    all-object Manager for InfiniteModel
    """
    queryset_class = qs.TruelyInfiniteQuerySet


class SoftDeleteInfiniteManager(InfiniteManager, SoftDeleteManager):
    """
    Manager for InfiniteModel
    """
    queryset_class = qs.InfiniteQuerySet

    def get_queryset(self):
        """
        Get all `hard-deleted` objects, time based objects
        """
        return self.queryset_class(self.model, using=self._db).filter(is_deleted=True)
