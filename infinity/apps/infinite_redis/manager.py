import redis
from django.conf import settings
from django.db.models.manager import BaseManager

from apps.infinite_redis.query import RedisQuerySet


# Redis DB
redis_ins = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    password=settings.REDIS_PASSWORD,
)


class RedisModelManager(BaseManager.from_queryset(RedisQuerySet)):
    """
    Since Our Model is abstract so all operations will be performed from here
    by using from_queryset we are adding all the methods of RedisQuerySet
    to this manager class
    """

    def __init__(self):
        super().__init__()

        self._db = redis_ins

    def bulk_upsert(self, data_dict):
        """bulk upsert using mset which takes in dict"""
        self._db.mset(data_dict)

    def save(self, instance, value):
        """custom save to update db"""
        self._db.set(instance.key, value)

    def delete(self, instance):
        """custom delete to update db"""
        self._db.delete(instance.key)
