from rest_framework import serializers
from .models import Package, Subscription


# Package Serializer
class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'


# Subscription Serializer
class SubscriptionSerializer(serializers.ModelSerializer):
    package = PackageSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'
