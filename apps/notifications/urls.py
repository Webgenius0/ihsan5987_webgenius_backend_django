from django.urls import path
from .views import (
    NotificationListView,
    UnreadNotificationCountView,
    MarkAsReadView,
    MarkAllAsReadView,
    RegisterDeviceView
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('unread-count/', UnreadNotificationCountView.as_view(), name='unread-count'),
    path('mark-all-as-read/', MarkAllAsReadView.as_view(), name='mark-all-read'),
    # path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('<int:pk>/mark-as-read/', MarkAsReadView.as_view(), name='mark-as-read'),
    path('register-device/', RegisterDeviceView.as_view(), name='register-device'),
]