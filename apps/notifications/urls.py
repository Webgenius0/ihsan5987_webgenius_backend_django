from django.urls import path
from .views import (
    NotificationListView,
    UnreadNotificationCountView,
    MarkAsReadView,
    MarkAllAsReadView,
    RegisterDeviceView,
    DeleteDeviceView,
    SystemNotificationListView,
    UnreadSystemNotificationCountView,
    MarkSystemNotificationAsReadView,
    MarkAllSystemNotificationsAsReadView
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('unread-count/', UnreadNotificationCountView.as_view(), name='unread-count'),
    path('mark-all-as-read/', MarkAllAsReadView.as_view(), name='mark-all-read'),
    # path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('<int:pk>/mark-as-read/', MarkAsReadView.as_view(), name='mark-as-read'),
    path('register-device/', RegisterDeviceView.as_view(), name='register-device'),
    path('device/delete/', DeleteDeviceView.as_view(), name='delete-device'),
    # System notifications
    path('system/', SystemNotificationListView.as_view(), name='system-notification-list'),
    path('system/unread-count/', UnreadSystemNotificationCountView.as_view(), name='system-unread-count'),
    path('system/mark-all-as-read/', MarkAllSystemNotificationsAsReadView.as_view(), name='system-mark-all-read'),
    path('system/<int:pk>/mark-as-read/', MarkSystemNotificationAsReadView.as_view(), name='system-mark-as-read'),
]