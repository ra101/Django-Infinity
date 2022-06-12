from rest_framework.serializers import ModelSerializer

from .models import ModelForTenant2


class SerializerForTenant2(ModelSerializer):
    class Meta:
        model = ModelForTenant2
        fields = ['id', 'data']
