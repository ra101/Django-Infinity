"""Command for creating public and private tenants"""
from decouple import config
from django.db.transaction import atomic
from apps.base import models
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Defines `initadmins` command that creates admin accounts"""

    domain = config('DOMAIN_URL', default='localhost')

    @atomic()
    def handle(self, *args, **options):
        """
        - Truncates old Auth Data
        - Create a SuperUser and GuestUser with ReadOnly Ablities
        - GuestUser: user/pass :: admin/admin
        """

        self.tuncate_tenant_models()

        self.create_tenant_domain(config('TENANT1_NAME', default='tenant1'))
        self.create_tenant_domain(config('TENANT2_NAME', default='tenant2'))

        self.create_public_domain()

    def tuncate_tenant_models(self):
        """
        Truncates Client and Domain Tables
        """

        return models.Tenant.objects.all().delete(), models.Domain.objects.all().delete()

    def create_tenant_domain(self, tenant_name):
        """
        Creates a Super User from .env
        """

        tenant_domain = models.Tenant.objects.create(schema_name=tenant_name)

        return models.Domain.objects.create(
            domain=f"{tenant_name}.{self.domain}",
            tenant=tenant_domain, is_primary = False
        )

    def create_public_domain(self):
        """
        Creates Group that can view all data but only change live_settings
        """
        public_tenant = models.Tenant.objects.create(schema_name='public')

        return models.Domain.objects.create(
            domain=self.domain, tenant=public_tenant, is_primary = True
        )
