from rest_framework.serializers import ModelSerializer

from .models import ModelForTenantShared


class SerializerForTenantShared(ModelSerializer):
    class Meta:
        model = ModelForTenantShared
        fields = ['id', 'data']
