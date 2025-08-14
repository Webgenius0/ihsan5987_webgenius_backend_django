from django.db import models
from apps.users.models import User

SUBSCRIPTION_TYPE = (
    ('year', 'Yearly'),
    ('month', 'Monthly'),
    ('week', 'Weekly'),
    ('day', 'Daily')
)


# Package Model
class Package(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True, null=True)
    interval = models.CharField(max_length=10, choices=SUBSCRIPTION_TYPE, default='month')
    stripe_product_id = models.CharField(max_length=100, blank=True)
    stripe_price_id = models.CharField(max_length=100, blank=True)
    discount = models.DecimalField(help_text='Set discount percentages.', max_digits=10, decimal_places=2, default=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    def get_discount_price(self):
        return self.price - (self.price * self.discount / 100)

    def save(self, *args, **kwargs):
        if self.discount > 0 and self.discount_price >= 0:
            self.discount_price = self.get_discount_price()
        else:
            self.discount_price = self.price
        super().save(*args, **kwargs)


# Subscription Model
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription_user')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='subscription_package')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} - {self.package.name}'
