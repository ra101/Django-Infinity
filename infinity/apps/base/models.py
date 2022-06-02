from django_tenants.models import TenantMixin, DomainMixin


class Tenant(TenantMixin):
    pass


class Domain(DomainMixin):
    pass
