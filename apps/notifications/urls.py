from django.urls import path
from .views import (
    NotificationListView,
    # UnreadNotificationCountView,
    # MarkAsReadView,
    # MarkAllAsReadView,
    # NotificationDetailView,
    RegisterDeviceView
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    # path('notifications/unread-count/', UnreadNotificationCountView.as_view(), name='unread-count'),
    # path('notifications/mark-all-as-read/', MarkAllAsReadView.as_view(), name='mark-all-read'),
    # path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    # path('notifications/<int:pk>/mark-as-read/', MarkAsReadView.as_view(), name='mark-as-read'),
    path('register-device/', RegisterDeviceView.as_view(), name='register-device'),
]