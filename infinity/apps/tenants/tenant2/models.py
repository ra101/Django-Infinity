from django.db.models import JSONField

from libs.models import TimeStampModel


class ExampleForTenant2(TimeStampModel):
    """
    Abstract model to maintain architecture of DRF
    """

    data = JSONField(default=dict)
