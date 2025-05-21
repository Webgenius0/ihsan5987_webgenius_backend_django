import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.decorators import method_decorator

from apps.users.models import User
from .models import Plan, Subscription
from .serializers import PlanSerializer


stripe.api_key = "sk_test_51RKXUyQwhEFKQj09gPsEy6T0ATHao5eAsc33mL7QV2caOHSAlRwH833FodKtC6SYliWXdDF0dcxEY6K0XJYZLceH00ZM5N9k1L"


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


class CreateSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get("plan_id")
        if not plan_id:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "plan_id is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Plan not found"
            }, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price": plan.stripe_price_id,
                    "quantity": 1,
                }],
                mode="subscription",
                success_url='http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://localhost:8000/cancel',
                customer_email=user.email,
            )

            return Response({
                "status": status.HTTP_200_OK,
                "success": True,
                "session_id": checkout_session.id,
                "url": checkout_session.url,
            })

        except stripe.error.StripeError as e:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": str(e),
            }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    if sig_header is None:
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        subscription_id = session['subscription']
        customer_email = session.get('customer_email')

        try:
            session_with_items = stripe.checkout.Session.retrieve(
                session['id'],
                expand=['line_items']
            )
            price_id = session_with_items['line_items']['data'][0]['price']['id']
            user = User.objects.get(email=customer_email)
            plan = Plan.objects.get(stripe_price_id=price_id)
            end_date = datetime.now() + timedelta(days=plan.duration_months * 30)

            Subscription.objects.update_or_create(
                user=user,
                plan=plan,
                defaults={
                    'stripe_subscription_id': subscription_id,
                    'is_active': True,
                    'end_date': end_date
                }
            )
        except (User.DoesNotExist, Plan.DoesNotExist, KeyError):
            return HttpResponse(status=400)

    return HttpResponse(status=200)
