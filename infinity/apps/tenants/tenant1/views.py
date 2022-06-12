from rest_framework.viewsets import ModelViewSet

from .serializers import SerializerForTenant1
from .models import ModelForTenant1


class ViewForTenant1(ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    serializer_class = SerializerForTenant1
    queryset = ModelForTenant1.objects.all()
