import json

import redis
from rest_framework import serializers
from django.conf import settings

from .models import RedisAbstractModel


# Get Instance of Redis Instance Used for Caching
redis_ins = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT,
    db=0, password=settings.REDIS_PASSWORD
)


class RedisInstanceSerializers(serializers.ModelSerializer):
    """
    For Retrieving, Updating and Deleleting
    """
    value = serializers.SerializerMethodField()

    class Meta:
        model = RedisAbstractModel
        fields = ['key', 'value']

    def to_internal_value(self, data):

        # resolve_key will append, api_ infront of each key
        data['key'] = self.resolve_key(self.instance.key)

        # We use json.dumps value so as to store every value as str
        # and restore type when json.loads is called
        data['value'] = json.dumps(data['value'])
        return super().to_internal_value(data)

    def save(self):
        redis_ins.set(self.initial_data['key'], self.initial_data['value'])

    def get_value(self, obj):
        value = redis_ins.get(obj.key)
        if value:
            return json.loads(value.decode("utf-8"))
        return value

    def resolve_key(self, key):
        return self.__class__._resolve_key(key)

    @staticmethod
    def _resolve_key(key):
        if not key.startswith("api_"):
            key = f"api_{key}"
        return key

    @staticmethod
    def delete(key):
        return redis_ins.delete(key)

    @staticmethod
    def is_key_valid(key):
        return bool(redis_ins.get(key))


class RedisBulkSerializer(serializers.Serializer):
    """
    For Listing and Bulk Creatiation
    """
    data = serializers.DictField()

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        str_data = {}

        # resolve each key and dump each value
        for key in data['data'].keys():
            new_key = key
            if not new_key.startswith("api_"):
                new_key = f"api_{new_key}"
            str_data[new_key] = json.dumps(data['data'][key])

        data['data'] = str_data

        return data

    def save(self):
        redis_ins.mset(self.validated_data['data'])

    def get_bulk_data(self):
        data = {}

        # get all keys with `api_` as prefix
        for key in redis_ins.keys("api_*"):
            data[key.decode("utf-8")] = json.loads(
                redis_ins.get(key).decode("utf-8")
            )
        return data
