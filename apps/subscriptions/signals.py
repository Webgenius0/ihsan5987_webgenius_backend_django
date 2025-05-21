import stripe
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Plan

stripe.api_key = settings.STRIPE_SECRET_KEY

@receiver(post_save, sender=Plan)
def create_stripe_price(sender, instance, created, **kwargs):
    if created and not instance.stripe_price_id:
        # 1. Create Stripe Product
        product = stripe.Product.create(name=instance.name)

        # 2. Determine recurring interval
        interval = "month" if instance.duration_months == 1 else "year" if instance.duration_months == 12 else None

        if interval is None:
            # Convert custom durations (e.g., 3 months) to month + interval_count
            recurring = {
                "interval": "month",
                "interval_count": instance.duration_months
            }
        else:
            recurring = {
                "interval": interval,
                "interval_count": 1
            }

        # 3. Create Stripe Price
        price = stripe.Price.create(
            unit_amount=int(instance.price * 100),  # cents
            currency="usd",
            recurring=recurring,
            product=product.id,
        )

        # 4. Save Stripe Price ID
        instance.stripe_price_id = price.id
        instance.save()
