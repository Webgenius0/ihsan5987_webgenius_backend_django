from django.urls import path
from .views import (
    GeneralNotificationListView,
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
    path('general/', GeneralNotificationListView.as_view(), name='general-notification-list'),
    path('general/unread-count/', UnreadNotificationCountView.as_view(), name='general-unread-count'),
    path('general/<int:pk>/mark-as-read/', MarkAsReadView.as_view(), name='general-mark-as-read'),
    path('general/mark-all-as-read/', MarkAllAsReadView.as_view(), name='general-mark-all-read'),
    path('register/device/', RegisterDeviceView.as_view(), name='register-device'),
    path('device/delete/', DeleteDeviceView.as_view(), name='delete-device'),

    # System notifications
    path('system/', SystemNotificationListView.as_view(), name='system-notification-list'),
    path('system/unread-count/', UnreadSystemNotificationCountView.as_view(), name='system-unread-count'),
    path('system/mark-all-as-read/', MarkAllSystemNotificationsAsReadView.as_view(), name='system-mark-all-read'),
    path('system/<int:pk>/mark-as-read/', MarkSystemNotificationAsReadView.as_view(), name='system-mark-as-read'),
]