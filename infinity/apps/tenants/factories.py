from factory import Faker
from factory.django import DjangoModelFactory

from .models import ModelForTenantShared


class FactoryForTenantShared(DjangoModelFactory):
    class Meta:
        model = ModelForTenantShared

    data = Faker("json")
