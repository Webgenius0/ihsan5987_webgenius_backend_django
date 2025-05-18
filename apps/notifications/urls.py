from django.urls import path
from .views import NotificationListAPIView, NotificationMarkAsReadAPIView, NotificationMarkAllAsReadAPIView, RegisterDeviceAPIView

urlpatterns = [
    path('', NotificationListAPIView.as_view(), name='notification-list'),
    path('<int:pk>/read/', NotificationMarkAsReadAPIView.as_view(), name='notification-mark-read'),
    path('mark-all-read/', NotificationMarkAllAsReadAPIView.as_view(), name='notification-mark-all-read'),
    path('register_device/', RegisterDeviceAPIView.as_view(), name='register-device'),
]