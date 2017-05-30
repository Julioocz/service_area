from rest_framework import serializers
from . import models


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Provider
        fields = '__all__'


class ServiceAreaSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)

    class Meta:
        model = models.ServiceArea
        fields = '__all__'
