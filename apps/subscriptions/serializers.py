from rest_framework import serializers
from .models import Plan, Subscription

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'duration_months']

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only = True)

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'plan', 'is_active', 'start_date', 'end_date']