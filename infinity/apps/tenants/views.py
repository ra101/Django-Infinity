from rest_framework.viewsets import ModelViewSet

from .serializers import SerializerForTenantShared
from .models import ModelForTenantShared


class ViewForTenantShared(ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    serializer_class = SerializerForTenantShared
    queryset = ModelForTenantShared.objects.all()
