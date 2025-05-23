from django.db import models
from apps.users.models import User


class Plan(models.Model):
    name = models.CharField(max_length=255)
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)  # allow blank
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.IntegerField()

    def __str__(self):
        return self.name
    
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscription")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="plan")
    stripe_subscription_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.user.name} - {self.plan.name}"