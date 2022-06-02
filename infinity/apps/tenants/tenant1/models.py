from django.db.models import JSONField

from libs.models import GhostModel


class ExampleForTenant1(GhostModel):
    """
    Abstract model to maintain architecture of DRF
    """

    data = JSONField(default=dict)
