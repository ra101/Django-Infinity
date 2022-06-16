from factory import Faker
from factory.django import DjangoModelFactory

from .models import ModelForTenant1


class FactoryForTenant1(DjangoModelFactory):
    class Meta:
        model = ModelForTenant1

    data = Faker("json")
