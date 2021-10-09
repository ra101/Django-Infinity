import json

from rest_framework import serializers

from .models import RedisAbstractModel


class RedisInstanceSerializers(serializers.ModelSerializer):
    """
    For Retrieving, Updating and Deleleting
    """

    class Meta:
        model = RedisAbstractModel
        fields = ["key", "value"]

    def to_representation(self, instance):
        return {
            instance.key.decode("utf-8"): json.loads(instance.value.decode("utf-8"))
        }

    def save(self, value):
        """
        Custom save for Calling Custom save of model (arg)
        """
        self.instance.save(value=json.dumps(value))


class RedisBulkUpsertSerializer(serializers.Serializer):
    """
    For Bulk Update or Create
    """

    def to_internal_value(self, data):
        dump_data = {}

        # resolve each key and dump each value
        for key in data.keys():
            new_key = key
            if not new_key.startswith("api_"):
                new_key = f"api_{key}"
            dump_data[new_key] = json.dumps(data[key])

        return dump_data

    def save(self):
        """
        Using cutom managers bulk_update instead of instance.save
        """
        RedisAbstractModel.objects.bulk_upsert(self.validated_data)
