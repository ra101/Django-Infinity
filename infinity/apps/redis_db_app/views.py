from django.http import Http404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import RedisAbstractModel
from .serializers import RedisBulkSerializer, RedisInstanceSerializers


class RedisDBAppViewSet(ModelViewSet):
    serializer_class = RedisInstanceSerializers
    queryset = RedisAbstractModel.objects.all()
    lookup_field = 'key'
    serializer_map = {
        'list': RedisBulkSerializer,
        'create': RedisBulkSerializer
    }

    def get_serializer_class(self):
        """
        BulkSerializer for listing and creating,
        rest uses InstanceSerializers
        """
        return self.serializer_map.get(self.action, self.serializer_class)

    def get_object(self):
        """
        Overriding `get_object` (check if key exists in redis db)
        for GET/UPDATE/DELETE (redis-db-app-details)
        """
        key = RedisInstanceSerializers._resolve_key(
            self.kwargs[self.lookup_field]
        )
        if not RedisInstanceSerializers.is_key_valid(key):
            raise Http404
        return RedisAbstractModel(key=key)

    def list(self, request, *args, **kwargs):
        """
        Overriding `list` (use redis search regex func)
        for GET (redis-db-app-list)
        """
        serializer = self.get_serializer()
        return Response(serializer.get_bulk_data())

    def perform_destroy(self, instance):
        """
        Overriding `perform_destroy` (delete via serializers)
        for DELETE (redis-db-app-details)
        """
        key = RedisInstanceSerializers._resolve_key(
            instance.key
        )
        RedisInstanceSerializers.delete(key)
