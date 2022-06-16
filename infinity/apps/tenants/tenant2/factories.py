from factory import Faker
from factory.django import DjangoModelFactory

from .models import ModelForTenant2


class FactoryForTenant2(DjangoModelFactory):
    class Meta:
        model = ModelForTenant2

    data = Faker("json")
