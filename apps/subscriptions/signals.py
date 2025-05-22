import stripe
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone
from .models import Plan, Subscription
import logging

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

# Signal to create Stripe Product and Price when a new Plan is created
@receiver(post_save, sender=Plan)
def create_stripe_price(sender, instance, created, **kwargs):
    if created and not instance.stripe_price_id:
        try:
            # 1. Create Stripe Product
            product = stripe.Product.create(name=instance.name)

            # 2. Determine recurring interval
            interval = "month" if instance.duration_months == 1 else "year" if instance.duration_months == 12 else None

            if interval is None:
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
                unit_amount=int(instance.price * 100),  # Convert to cents
                currency="usd",
                recurring=recurring,
                product=product.id,
            )

            # 4. Save Stripe Price ID
            instance.stripe_price_id = price.id
            instance.save(update_fields=['stripe_price_id'])
            logger.info(f"Created Stripe price {price.id} for plan {instance.name}")
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create Stripe price for plan {instance.name}: {e}")

# Existing signal to update subscriptions when a plan's price or duration changes
@receiver(pre_save, sender=Plan)
def update_subscriptions_on_plan_change(sender, instance, **kwargs):
    try:
        old_plan = Plan.objects.get(pk=instance.pk) if instance.pk else None
        if old_plan and (old_plan.price != instance.price or old_plan.duration_months != instance.duration_months):
            subscriptions = Subscription.objects.filter(plan=instance, active=True)
            for subscription in subscriptions:
                days = instance.duration_months * 30
                new_end_date = subscription.start_date + timezone.timedelta(days=days)
                subscription.end_date = new_end_date
                subscription.save(update_fields=['end_date'])
                logger.info(f"Updated subscription {subscription.id} end_date to {new_end_date} due to plan change.")
    except Plan.DoesNotExist:
        pass

# Existing signal to notify admins when a new plan is added
@receiver(post_save, sender=Plan)
def notify_plan_creation(sender, instance, created, **kwargs):
    if created:
        subject = "New Plan Created"
        message = f"""
        A new plan has been added:
        - Name: {instance.name}
        - Price: ${instance.price}
        - Duration: {instance.duration_months} months
        - Stripe Price ID: {instance.stripe_price_id}
        Created at: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        from_email = "noreply@yourdomain.com"
        recipient_list = ["admin@yourdomain.com"]
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            logger.info(f"Notification sent for new plan: {instance.name}")
        except Exception as e:
            logger.error(f"Failed to send notification for plan {instance.name}: {e}")

# Existing signal to log subscription switches
@receiver(post_save, sender=Subscription)
def log_subscription_switch(sender, instance, created, **kwargs):
    if not created:
        try:
            old_subscription = Subscription.objects.get(pk=instance.pk)
            if old_subscription.plan_id != instance.plan_id:
                logger.info(f"Subscription {instance.id} switched to plan {instance.plan.name} at {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except Subscription.DoesNotExist:
            pass