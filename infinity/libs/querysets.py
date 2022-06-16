from django.db.models.signals import pre_delete, post_delete

from model_utils.managers import JoinQueryset
from psqlextra.query import PostgresQuerySet
from polymorphic.query import PolymorphicQuerySet, PolymorphicModelIterable
from timescale.db.models.querysets import TimescaleQuerySet


class PSQLExtraQuerySet(PostgresQuerySet, JoinQueryset):
    pass


class SoftDeleteQuerySet(PSQLExtraQuerySet):
    """
    QuerySet for SoftDeleteManager
    """

    def delete(self):
        """
        `soft-delete` the object, so it can restoreed later.
        """

        for obj in self:
            pre_delete.send(sender=obj.__class__, instance=obj)

        self.update(is_deleted=False)

        for obj in self:
            post_delete.send(sender=obj.__class__, instance=obj)

    def hard_delete(self):
        """
        Permanently delete all the objects in queryset.
        """

        return super().delete()

    def restore(self):
        """
        Restore all the `soft-deleted` all the objects in queryset.
        """

        self.update(is_deleted=True)


class PolymorphicExtraQuerySet(PSQLExtraQuerySet, PolymorphicQuerySet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._iterable_class = PolymorphicModelIterable

        self.polymorphic_disabled = False
        self.polymorphic_deferred_loading = (set(), True)

    def annotate(self, *args, **kwargs):
        self._process_aggregate_args(args, kwargs)
        return super().annotate(*args, **kwargs)


class TimeScaleQuerySet(PSQLExtraQuerySet, TimescaleQuerySet):
    """
    Queryset for TimeScaleManager, time_scale + psql_extra
    """
    pass


class TruelyInfiniteQuerySet(PolymorphicExtraQuerySet, TimeScaleQuerySet):
    """
    QuerySet for InfiniteManager
    """
    pass


class InfiniteQuerySet(TruelyInfiniteQuerySet, SoftDeleteQuerySet):
    """
    QuerySet for SoftDeleteInfiniteManager
    """
    pass
