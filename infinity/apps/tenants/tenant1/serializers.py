from rest_framework.serializers import ModelSerializer

from .models import ModelForTenant1


class SerializerForTenant1(ModelSerializer):
    class Meta:
        model = ModelForTenant1
        fields = ['id', 'data']
