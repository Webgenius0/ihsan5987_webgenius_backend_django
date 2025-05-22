import stripe
import logging
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.decorators import method_decorator
import stripe.error

from apps.users.models import User
from .models import Plan, Subscription
from .serializers import PlanSerializer, SubscriptionSerializer


stripe.api_key = "sk_test_51RKXUyQwhEFKQj09gPsEy6T0ATHao5eAsc33mL7QV2caOHSAlRwH833FodKtC6SYliWXdDF0dcxEY6K0XJYZLceH00ZM5N9k1L"
logger = logging.getLogger(__name__)


class PlanListView(APIView):
    def get(self, request, *args, **kwargs):
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Plans retrieved successfully",
            "data": serializer.data
        })


#  Create Subscription View
class CreateSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        plan_id = request.data.get('plan_id')
        if not plan_id:
            return Response({"error": "plan_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # Check for existing active subscription
        active_subscription = Subscription.objects.filter(user=user, is_active=True).first()
        if active_subscription:
            serializer = SubscriptionSerializer(active_subscription)
            return Response({
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "You already have an active subscription",
                "subscription": serializer.data
            }, status=status.HTTP_200_OK)
        
        # Check for an existing pending Checkout Session
        try:
            existing_sessions = stripe.checkout.Session.list(
                customer_email=user.email,
                status='open',
                limit=1
            ).data
            if existing_sessions:
                existing_session = existing_sessions[0]
                if datetime.fromtimestamp(existing_session.expires_at) > datetime.now():
                    return Response({
                        'status': status.HTTP_200_OK,
                        'success': True,
                        'session_id': existing_session.id,
                        'url': existing_session.url
                    }, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            logger.warning(f"Failed to check existing sessions for user {user.email}: {e}")

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': plan.stripe_price_id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url='http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://localhost:8000/cancel',
                customer_email=user.email,
            )
            return Response({
                'status': status.HTTP_200_OK,
                'success': True,
                'session_id': checkout_session.id,
                'url': checkout_session.url
            }, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            logger.error(f"Failed to create checkout session for user {user.email}: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# Switch subscription plan
class SwitchSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logger.debug(f"Request data: {request.data}")
        new_plan_id = request.data.get('new_plan_id')
        
        if not new_plan_id:
            logger.error("new_plan_id is missing in request data")
            return Response({"error": "new_plan_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_plan = Plan.objects.get(id=new_plan_id)
        except Plan.DoesNotExist:
            logger.error(f"Plan with id {new_plan_id} not found")
            return Response({"error": "New plan not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # Fetch the user's active subscription (Plan 1)
        old_subscription = Subscription.objects.filter(user=user, is_active=True).first()
        if not old_subscription:
            logger.error(f"No active subscription found for user {user.email}")
            return Response({"error": "No active subscription found to switch from"}, status=status.HTTP_404_NOT_FOUND)

        if old_subscription.plan_id == new_plan_id:
            logger.warning(f"User {user.email} attempted to switch to the same plan {new_plan_id}")
            return Response({"error": "You are already subscribed to this plan"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the customer and their default payment method
        try:
            customer = stripe.Customer.list(email=user.email).data
            if not customer:
                logger.error(f"No Stripe customer found for user {user.email}")
                return Response({"error": "No Stripe customer found"}, status=status.HTTP_400_BAD_REQUEST)
            customer = customer[0]

            # Retrieve the old subscription
            old_stripe_subscription = stripe.Subscription.retrieve(old_subscription.stripe_subscription_id)

            # Try to get the customer's default payment method
            default_payment_method = customer.get("invoice_settings", {}).get("default_payment_method")

            # Fallback: fetch the most recently attached payment method if default not set
            if not default_payment_method:
                payment_methods = stripe.PaymentMethod.list(
                    customer=customer.id,
                    type="card"
                )
            if payment_methods.data:
                default_payment_method = payment_methods.data[0].id

            if not default_payment_method:
                logger.error(f"No default payment method found for customer {customer.id}")
                return Response({"error": "A payment method is required to create a new subscription"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            logger.error(f"Failed to retrieve customer or payment method for user {user.email}: {e}")
            return Response({"error": f"Failed to retrieve customer: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Cancel the old subscription in Stripe and set is_active=False in the database
        try:
            stripe.Subscription.cancel(old_subscription.stripe_subscription_id)
            old_subscription.is_active = False
            old_subscription.save(update_fields=['is_active'])
            logger.info(f"Canceled subscription {old_subscription.stripe_subscription_id} for user {user.email}")
        except stripe.error.StripeError as e:
            logger.error(f"Failed to cancel subscription {old_subscription.stripe_subscription_id}: {e}")
            return Response({"error": f"Failed to cancel existing subscription: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new subscription in Stripe for the new plan (Plan 2)
        try:
            new_stripe_subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{'price': new_plan.stripe_price_id}],
                default_payment_method=default_payment_method,  # Reuse the payment method
                payment_behavior='allow_incomplete',  # Allow creation even if payment fails
                proration_behavior='create_prorations',
            )
            logger.info(f"Created new subscription {new_stripe_subscription.id} for user {user.email}")
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create new subscription for user {user.email}: {e}")
            return Response({"error": f"Failed to create new subscription: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new subscription in the database for Plan 2
        days = new_plan.duration_months * 30
        new_subscription = Subscription.objects.create(
            user=user,
            plan=new_plan,
            stripe_subscription_id=new_stripe_subscription.id,
            is_active=True,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=days)
        )
        logger.info(f"Created new database subscription {new_subscription.id} for plan {new_plan.name}")

        # Return the new subscription details
        serializer = SubscriptionSerializer(new_subscription)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Plan switched successfully",
            "subscription": serializer.data
        }, status=status.HTTP_200_OK)
        
# Webhook
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        logger.error(f"Webhook ValueError: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Webhook SignatureVerificationError: {e}")
        return HttpResponse(status=400)

    # Handle successful subscription creation
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session['customer_email']
        subscription_id = session['subscription']

        try:
            retrieved_session = stripe.checkout.Session.retrieve(session.id, expand=['line_items'])
            line_items = retrieved_session.line_items.data
            if not line_items:
                raise ValueError("No line items found in session")
            price_id = line_items[0].price.id

            user = User.objects.get(email=customer_email)
            plan = Plan.objects.get(stripe_price_id=price_id)

            end_date = datetime.now() + timedelta(days=plan.duration_months * 30)
            Subscription.objects.update_or_create(
                user=user,
                stripe_subscription_id=subscription_id,
                defaults={'plan': plan, 'end_date': end_date, 'is_active': True}
            )
            logger.info(f"Created subscription {subscription_id} for user {customer_email}")
        except (User.DoesNotExist, Plan.DoesNotExist, ValueError) as e:
            logger.error(f"Webhook error processing session {session.id}: {e}")
            return HttpResponse(status=400)

    # Handle subscription cancellation or status update
    elif event['type'] in ['customer.subscription.updated', 'customer.subscription.deleted']:
        subscription_data = event['data']['object']
        stripe_sub_id = subscription_data['id']
        status = subscription_data['status']

        try:
            subscription = Subscription.objects.get(stripe_subscription_id=stripe_sub_id)
            if status == 'canceled' or status == 'unpaid':
                subscription.is_active = False
                subscription.save(update_fields=['is_active'])
                logger.info(f"Deactivated subscription {stripe_sub_id} due to status {status}")
        except Subscription.DoesNotExist:
            logger.warning(f"Subscription {stripe_sub_id} not found in database")
            return HttpResponse(status=400)

    # Handle successful payment method setup
    elif event['type'] == 'setup_intent.succeeded':
        setup_intent = event['data']['object']
        customer_id = setup_intent['customer']
        payment_method = setup_intent['payment_method']
        logger.info(f"Payment method {payment_method} added for customer {customer_id}")
        # Optionally notify the user or log for further action

    return HttpResponse(status=200)