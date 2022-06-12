from rest_framework.viewsets import ModelViewSet

from .serializers import SerializerForTenant2
from .models import ModelForTenant2


class ViewForTenant2(ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    serializer_class = SerializerForTenant2
    queryset = ModelForTenant2.objects.all()
