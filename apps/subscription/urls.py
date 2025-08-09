from django.urls import path
from .views import PackageView, SubscriptionView, SubscriptionCreate, CancelSubscription, UserActiveSubscriptionView, stripe_webhook_view

urlpatterns = [
    path('packages/', PackageView.as_view(), name='package-list'),
    path('package/<int:pk>/', PackageView.as_view(), name='package-detail'),

    path('subscription-list/', SubscriptionView.as_view(), name='subscription-list'),
    path('user/active-subscription/', UserActiveSubscriptionView.as_view(), name='user-active-subscription'),
    path('subscription/<int:package_id>/', SubscriptionView.as_view(), name='subscription-detail'),

    path('subscribe/<int:package_id>/', SubscriptionCreate.as_view(), name='subscription-create'),
    path('cancel/<int:subscription_id>/', CancelSubscription.as_view(), name='cancel-subscription'),

    path('webhook/', stripe_webhook_view, name='stripe-webhook'),
]
