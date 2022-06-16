import uuid, requests

from django.db.transaction import atomic
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models
from timescale.db.models.fields import TimescaleDateTimeField
from polymorphic.models import PolymorphicModel
from simple_history.models import HistoricalRecords
from simple_history.signals import pre_create_historical_record
from model_utils.tracker import FieldTracker

from . import managers


class HistoryModel(HistoricalRecords):

    class BaseModel(models.Model):

        history_ip = models.GenericIPAddressField(null=True, default=None)
        history_loc = models.PointField(null=True, default=None)

        class Meta:
            abstract = True

        @staticmethod
        def populate_history_ip_loc(sender, **kwargs):

            try:
                if HistoricalRecords.context.request:
                    request_meta = HistoricalRecords.context.request.META
            except AttributeError:
                return None

            ip_addr = request_meta.get(
                'HTTP_X_FORWARDED_FOR', request_meta.get('REMOTE_ADDR')
            ).split(',')[0]

            if not ip_addr:
                return None

            kwargs['history_instance'].history_ip = ip_addr

            x, y, GEOLOCATION_URL = None, None, "https://geolocation-db.com/json/{0}"

            try:
                response = requests.get(GEOLOCATION_URL.format(ip_addr))
            except Exception:
                return None

            if response.status_code != 200:
                return None

            x, y = response.json().get('longitude'), response.json().get('latitude')
            if isinstance(x, float) and isinstance(y, float):
                kwargs['history_instance'].history_loc = Point(x, y)

    def __init__(self, *args, **kwrags):
        super().__init__(*args, **kwrags)
        self.bases = (self.BaseModel, )

    def get_extra_fields(self, model, fields):
        extra_fields = super().get_extra_fields(model, fields)
        extra_fields.update({
            "history_date": TimescaleDateTimeField(
                db_index=self._date_indexing is True, interval="1 day"
            )
        })
        return extra_fields

    def post_delete(self, instance, using=None, **kwargs):
        with atomic():
            # delete history for hard_delete, else keep it
            self.cascade_delete_history = not kwargs.get('soft_delete', False)
            super().post_delete(instance, using, **kwargs)


pre_create_historical_record.connect(
    HistoryModel.BaseModel.populate_history_ip_loc,
    sender=HistoryModel
)


class TimeStampModel(models.Model):
    """
    Keeps a record of created and last-updated date-time
     - Uses TimescaleDB for extensive Queryset
    """

    created_on = TimescaleDateTimeField(auto_now_add=True, interval="1 day", editable=False)
    updated_on = TimescaleDateTimeField(auto_now=True, interval="1 day", editable=False)

    objects = models.Manager()
    timescale = managers.TimeScaleManager()

    class Meta:
        """
        Meta class for TimeStampModel
        """

        abstract = True


class PSQLExtraModel(models.Model):
    """
    Base class for for taking advantage of PostgreSQL specific features.
    """

    objects = managers.PSQLExtraManager()

    class Meta:
        """
        Meta class for PSQLExtraModel
        """

        abstract = True


class SoftDeleteModel(models.Model):
    """
    AfterLife for removed records.
     - Once deleted from here, Soul itself gets detroyed!
    """

    is_deleted = models.BooleanField(default=True, editable=False)

    objects = managers.SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, *args, **kwargs):
        """
        Method to `soft-delete` an object.
        """

        # A soft_delete flag is passed for keeping signals in check
        signal_args = dict(sender=self.__class__, instance=self, soft_delete=True)

        with atomic(savepoint=False):

            models.signals.pre_delete.send(**signal_args)

            # Don't use .save() otherwise it will trigger save signals
            self.__class__.all_objects.filter(id=self.id).update(is_deleted=False)

            models.signals.post_delete.send(**signal_args)

    def restore(self):
        """
        Restore `soft-deleted` objects.
        """

        self.__class__.all_objects.filter(id=self.id).update(is_deleted=True)

    def hard_delete(self, using=None):
        """
        Permanently delete the objects.
        """

        return super().delete(using)

    class Meta:
        """
        Meta class for SoftDeleteModel
        """

        abstract = True


class PolymorphicExtraModel(PolymorphicModel):

    objects = managers.PolymorphicExtraManager()

    class Meta(PolymorphicModel.Meta):
        """
        Meta class for PolymorphicExtraModel
        """

        abstract = True


class InfiniteModel(PolymorphicExtraModel, TimeStampModel, SoftDeleteModel):
    """
    Inhereted from TimeStamp and SoftDeleteModel
     - fields: `id:uuid`, `is_deleted`
     - utils: `tracker`
     - managers: `objects`, `timescale`, `all_objects`, `history`
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    tracker = FieldTracker()

    objects = managers.SoftDeleteInfiniteManager()
    all_objects = managers.InfiniteManager()

    updated_on, created_on = None, None

    history = HistoryModel(inherit=True, excluded_fields=['id', 'is_deleted'])

    class Meta(PolymorphicModel.Meta):
        """
        Meta class for InfiniteModel
        """

        abstract = True
