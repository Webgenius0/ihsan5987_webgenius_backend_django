from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Notification
from .serializers import GeneralNotificationSerializer, NotificationUpdateSerializer, SystemNotificationSerializer
from fcm_django.models import FCMDevice
from django.shortcuts import get_object_or_404

class GeneralNotificationListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            notifications = Notification.objects.filter(recipient=request.user, category='general').order_by('-created_at')
            serializer = GeneralNotificationSerializer(notifications, many=True)
            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "General Notification fetched successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(f"Error in GeneralNotificationListView: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UnreadNotificationCountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Unread notification count fetched successfully",
            'unread_count': count
            }, status=status.HTTP_200_OK)

class MarkAsReadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, recipient=request.user)

        # Force update `is_read` to True
        notification.is_read = True
        notification.save()

        serializer = NotificationUpdateSerializer(notification, data=request.data, partial=True)
            
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Notification marked as read successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MarkAllAsReadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        updated = Notification.objects.filter(
            recipient=request.user, 
            is_read=False
        ).update(is_read=True)
        
        return Response(
            {
                "success": True,
                "message": f"{updated} notifications marked as read",
            },
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
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Device registered successfully",
            }, status=status.HTTP_200_OK)
    
    
class DeleteDeviceView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        registration_id = request.data.get('registration_id')
        if not registration_id:
            return Response({'error': 'registration_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            device = FCMDevice.objects.get(user=request.user, registration_id=registration_id)
            device.delete()
            return Response({
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Device deleted successfully",
                }, status=status.HTTP_200_OK)
        
        except FCMDevice.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Device not found",
                }, status=status.HTTP_404_NOT_FOUND)
        

# System notifications
class SystemNotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(
            recipient=request.user,
            category='system'
        ).order_by('-created_at')
        serializer = SystemNotificationSerializer(notifications, many=True)
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
