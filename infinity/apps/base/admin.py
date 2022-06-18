from django.contrib import admin
from unittest.mock import patch

from redis.client import Pipeline
from redisboard.models import RedisServer
from redisboard.admin import RedisServerAdmin
from django_tenants.admin import TenantAdminMixin

from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    pass


admin.site.unregister(RedisServer)


@admin.register(RedisServer)
class ExtendedRedisServerAdmin(RedisServerAdmin):
    """
    - Removing URL and Password field from admin,
        Since Auther of redisboard did not use password fields,
    - updateing inspect view to work with new redis package
    """

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            fields = [field for field in fields if field not in ["url", "password"]]
        return fields

    def inspect_view(self, request, server, db=None, cursor=0):
        """
        Mocking command that do not exists
        """

        def mock_select(db=0):
            pass

        server.connection.select = mock_select

        def pipeline(transaction=True, shard_hint=None):

            pipeline = Pipeline(
                server.connection.connection_pool,
                server.connection.response_callbacks,
                transaction,
                shard_hint,
            )

            pipeline.select = mock_select
            return pipeline

        server.connection.pipeline = pipeline
        return super().inspect_view(request, server, db, cursor)

    def inspect_key_view(self, request, server, db, key, cursor=0, count=0):
        """
        Mocking command that do not exists
        """

        def mock_select(db=0):
            pass

        server.connection.select = mock_select

        def pipeline(transaction=True, shard_hint=None):

            pipeline = Pipeline(
                server.connection.connection_pool,
                server.connection.response_callbacks,
                transaction,
                shard_hint,
            )

            pipeline.select = mock_select
            return pipeline

        server.connection.pipeline = pipeline
        return super().inspect_key_view(request, server, db, key, cursor, count)
