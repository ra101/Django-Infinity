from django.http.response import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from .models import RedisAbstractModel
from .serializers import RedisInstanceSerializers, RedisBulkUpsertSerializer


class InfiniteRedisViewSet(ModelViewSet):
    """
    View for Infinite Redis
    """

    serializer_class = RedisInstanceSerializers
    queryset = RedisAbstractModel.objects.filter(key="api_*")
    lookup_field = "key"
    serializer_map = {"create": RedisBulkUpsertSerializer}

    def get_object(self):
        """
        Resolving key and using custom Manager to return obj
        """

        # resolve each key
        key = self.kwargs["key"]
        if not key.startswith("api_"):
            self.kwargs["key"] = f"api_{key}"

        try:
            obj = RedisAbstractModel.objects.get(key=key)
        except Exception:
            raise Http404

        return obj

    def get_serializer_class(self):
        """
        BulkSerializer for creating/updating,
        rest uses InstanceSerializers
        """
        return self.serializer_map.get(self.action, self.serializer_class)

    def list(self, request, *args, **kwargs):
        """
        Parse List of dicts to a single big dict
        """

        ret = super().list(request, *args, **kwargs)

        # [{}, {}, ...] -> {...}
        if ret.data:
            data = {}
            for single_dict in ret.data:
                data.update(single_dict)
            ret.data = data
        return ret

    def perform_update(self, serializer):
        """
        Override this function to call serializer.save with arg
        """
        if not self.request.data.get("value"):
            raise ValidationError("`value` is a required field")
        serializer.save(self.request.data["value"])
