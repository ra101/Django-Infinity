from django.db.models import query, QuerySet
from django.core.exceptions import FieldError


class RedisIterable(query.BaseIterable):
    """
    ModelIterable: how fetching is done, used by all, filter, exclude or any query operation
    """

    def __iter__(self):
        """Only one but essential function"""

        # Get Constants
        queryset = self.queryset
        model = queryset.model
        query = queryset.query
        redis_instance = queryset.db  # RedisModelManager._db

        pattern = "*"

        # check if filter is used (else all() is used)
        if query.where.children:
            try:
                pattern = query.where.children[0].rhs
            except Exception:
                return None

        result = {}
        for key in redis_instance.keys(pattern):
            result[key] = redis_instance.get(key)

        # low_mark and high_mark are the indexs of queryset
        for key, value in list(result.items())[query.low_mark: query.high_mark]:
            yield model(key=key, value=value)


class RedisQuerySet(QuerySet):
    """
    Need to define custom QuerySet to work with custom iterable
    """

    def __init__(self, model=None, query=None, using=None, hints=None):
        """Everything same but Update the _iterable_class"""
        super().__init__(model=model, query=query, using=using, hints=hints)
        self._iterable_class = RedisIterable

    def filter(self, *args, **kwargs):
        """
        Parsing data, Not implementing anthing, Only allowed query is __eq__
        """

        # get first element of filter kwargs
        key, value = next(iter(kwargs.items()))

        # seprate key and rest of conditions
        key, *query = key.split("__")

        if key != "key":
            raise FieldError(
                f"Cannot resolve keyword {key} into field. Only choice is `key`"
            )

        # Only __eq__ alowed, so raise error if any key found
        if query:
            raise FieldError(f"Unsupported lookup {'__'.join(query)} for {self.model}")

        return super().filter(*args, **{"key": value})

    def exclude(self, *args, **kwargs):
        """Redis do not allow exclude"""
        raise AttributeError("'RedisQuerySet' object has no attribute 'exclude'")
