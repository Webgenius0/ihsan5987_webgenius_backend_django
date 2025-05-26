import stripe
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Package, Subscription
from .serializers import PackageSerializer, SubscriptionSerializer
from apps.users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class PackageView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                package = Package.objects.get(pk=pk)
                serializer = PackageSerializer(package)
                return Response({
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Package retrieved successfully",
                    "data": serializer.data
                })
            except Package.DoesNotExist:
                return Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": "Package not found"
                }, status=status.HTTP_404_NOT_FOUND)

        packages = Package.objects.all()
        serializer = PackageSerializer(packages, many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "All packages retrieved successfully",
            "data": serializer.data
        })


class SubscriptionView(APIView):
    def get(self, request, package_id=None):
        if package_id:
            try:
                subscription = Subscription.objects.get(id=package_id)
                serializer = SubscriptionSerializer(subscription)
                return Response({
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": "Subscription retrieved successfully",
                    "data": serializer.data
                })
            except Subscription.DoesNotExist:
                return Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": "Subscription not found"
                }, status=status.HTTP_404_NOT_FOUND)

        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "All subscriptions retrieved successfully",
            "data": serializer.data
        })


class SubscriptionCreate(APIView):
    def post(self, request, package_id):
        user = request.user
        try:
            package = Package.objects.get(id=package_id)
        except Package.DoesNotExist:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'success': False,
                'message': 'Package not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            customers = stripe.Customer.list(email=user.email)
            stripe_customer = customers.data[0] if customers.data else stripe.Customer.create(
                email=user.email,
                name=f'{user.first_name} {user.last_name}'
            )
        except stripe.error.StripeError as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'success': False,
                'message': 'Stripe customer creation failed',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        current_subscription = Subscription.objects.filter(user=user, is_active=True).first()

        if current_subscription:
            try:
                stripe_subscription = stripe.Subscription.retrieve(current_subscription.stripe_subscription_id)
                stripe.Subscription.modify(
                    stripe_subscription.id,
                    items=[{
                        'id': stripe_subscription['items']['data'][0].id,
                        'price': package.stripe_price_id
                    }],
                    proration_behavior='create_prorations',
                )
                updated = stripe.Subscription.retrieve(stripe_subscription.id)
                current_subscription.is_active = False
                current_subscription.save()

                new_sub = Subscription.objects.create(
                    user=user,
                    package=package,
                    stripe_subscription_id=updated.id,
                    end_date=datetime.fromtimestamp(updated['items']['data'][0]['current_period_end']),
                    is_active=True
                )
                return Response({
                    'status': status.HTTP_200_OK,
                    'success': True,
                    'message': 'Subscription updated successfully.',
                    'data': SubscriptionSerializer(new_sub).data
                })
            except stripe.error.StripeError as e:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'message': 'Failed to update subscription.',
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='subscription',
                line_items=[{
                    'price': package.stripe_price_id,
                    'quantity': 1
                }],
                customer=stripe_customer.id,
                success_url=settings.STRIPE_SUCCESS_URL,
                cancel_url=settings.STRIPE_CANCEL_URL,
                metadata={
                    'user_id': str(user.id),
                    'package_id': str(package.id)
                },
                subscription_data={
                    'metadata': {
                        'user_id': str(user.id),
                        'package_id': str(package.id)
                    }
                }
            )
            return Response({
                'status': status.HTTP_200_OK,
                'success': True,
                'message': 'Checkout session created successfully.',
                'data': {
                    'url': session.url
                }
            })
        except stripe.error.StripeError as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'success': False,
                'message': 'Failed to create checkout session.',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class CancelSubscription(APIView):
    def post(self, request, subscription_id):
        user = request.user
        try:
            subscription = Subscription.objects.get(id=subscription_id, user=user)
        except Subscription.DoesNotExist:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'success': False,
                'message': 'Subscription not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            stripe.Subscription.cancel(subscription.stripe_subscription_id)
            subscription.is_active = False
            subscription.save()
            return Response({
                'status': status.HTTP_200_OK,
                'success': True,
                'message': 'Subscription cancelled successfully.'
            })
        except stripe.error.StripeError as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'success': False,
                'message': 'Failed to cancel subscription.',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_KEY

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        return HttpResponse(status=400)

    data = event['data']['object']
    event_type = event['type']

    try:
        if event_type == 'customer.subscription.created':
            metadata = data.get('metadata', {})
            user_id = metadata.get('user_id')
            package_id = metadata.get('package_id')
            if not user_id or not package_id:
                raise ValueError("Missing metadata")

            user = User.objects.get(id=user_id)
            package = Package.objects.get(id=package_id)

            Subscription.objects.create(
                user=user,
                package=package,
                stripe_subscription_id=data['id'],
                end_date=datetime.fromtimestamp(data['current_period_end']),
                is_active=True
            )

        elif event_type == 'customer.subscription.updated':
            metadata = data.get('metadata', {})
            user_id = metadata.get('user_id')
            package_id = metadata.get('package_id')

            user = User.objects.get(id=user_id)
            package = Package.objects.get(id=package_id)

            Subscription.objects.filter(
                user=user, package=package
            ).update(
                stripe_subscription_id=data['id'],
                end_date=datetime.fromtimestamp(data['current_period_end'])
            )

        elif event_type == 'customer.subscription.deleted':
            Subscription.objects.filter(
                stripe_subscription_id=data['id']
            ).update(is_active=False)

        else:
            print(f"Unhandled event type: {event_type}")

    except Exception as e:
        print(f"Error handling webhook: {e}")
        return HttpResponse(status=500)

    return HttpResponse(status=200)
