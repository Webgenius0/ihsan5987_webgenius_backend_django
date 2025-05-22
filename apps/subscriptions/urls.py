from django.urls import path
from .views import PlanListView, CreateSubscriptionView, SwitchSubscriptionView ,stripe_webhook

urlpatterns = [
    path('plans/', PlanListView.as_view(), name='plan-list'),
    path('create-subscription/', CreateSubscriptionView.as_view(), name='create-subscription'),
    path('switch-plan/', SwitchSubscriptionView.as_view(), name='switch-plan'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
]
