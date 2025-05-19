from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer
from fcm_django.models import FCMDevice

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        response = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Notification fetched successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


# class NotificationMarkAsReadView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk):
#         try:
#             notification = Notification.objects.get(pk=pk, recipient=request.user)
#             notification.is_read = True
#             notification.save()
#             return Response({"detail": "Notification marked as read"}, status=status.HTTP_200_OK)
#         except Notification.DoesNotExist:
#             return Response({"detail": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)


# class NotificationMarkAllAsReadView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
#         return Response({"detail": "All notifications marked as read"}, status=status.HTTP_200_OK)


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