from django.urls import path
from .views import PackageView, SubscriptionView, SubscriptionCreate, CancelSubscription, stripe_webhook_view

urlpatterns = [
    path('packages/', PackageView.as_view(), name='package-list'),
    path('packages/<int:pk>/', PackageView.as_view(), name='package-detail'),

    path('subscriptions/', SubscriptionView.as_view(), name='subscription-list'),
    path('subscriptions/<int:package_id>/', SubscriptionView.as_view(), name='subscription-detail'),

    path('subscribe/<int:package_id>/', SubscriptionCreate.as_view(), name='subscription-create'),
    path('cancel/<int:subscription_id>/', CancelSubscription.as_view(), name='cancel-subscription'),

    path('webhook/', stripe_webhook_view, name='stripe-webhook'),
]
