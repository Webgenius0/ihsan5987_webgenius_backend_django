from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer, NotificationUpdateSerializer
from fcm_django.models import FCMDevice
from django.shortcuts import get_object_or_404

class GeneralNotificationListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user, category='general').order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        response = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "General Notification fetched successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class UnreadNotificationCountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return Response({'unread_count': count}, status=status.HTTP_200_OK)

class MarkAsReadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
        serializer = NotificationUpdateSerializer(notification, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MarkAllAsReadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        updated = Notification.objects.filter(
            recipient=request.user, 
            is_read=False
        ).update(is_read=True)
        
        return Response(
            {'detail': f'{updated} notifications marked as read'},
            status=status.HTTP_200_OK
        )


class RegisterDeviceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        registration_id = request.data.get('registration_id')
        if not registration_id:
            return Response({'error': 'registration_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        FCMDevice.objects.update_or_create(
            user=request.user,
            registration_id=registration_id,
            defaults={'active': True, 'type': 'web'}
        )
        return Response({'status': 'device registered'}, status=status.HTTP_200_OK)
    
    
class DeleteDeviceView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        registration_id = request.data.get('registration_id')
        if not registration_id:
            return Response({'error': 'registration_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            device = FCMDevice.objects.get(user=request.user, registration_id=registration_id)
            device.delete()
            return Response({'status': 'device deleted'}, status=status.HTTP_200_OK)
        except FCMDevice.DoesNotExist:
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
        

# System notifications
class SystemNotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(
            recipient=request.user,
            category='system'
        ).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "System notifications fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class UnreadSystemNotificationCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = Notification.objects.filter(
            recipient=request.user, 
            category='system', 
            is_read=False
        ).count()
        return Response({'unread_count': count}, status=status.HTTP_200_OK)


class MarkSystemNotificationAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, recipient=request.user, category='system')
        notification.is_read = True
        notification.save()
        return Response({'detail': 'Notification marked as read'}, status=status.HTTP_200_OK)


class MarkAllSystemNotificationsAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        updated = Notification.objects.filter(
            recipient=request.user, category='system', is_read=False
        ).update(is_read=True)
        return Response({'detail': f'{updated} system notifications marked as read'}, status=status.HTTP_200_OK)
