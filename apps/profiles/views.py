from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer
from .models import Profile

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)

        except Profile.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Profile not found",
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSerializer(profile)
        response = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Profile retrieved successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Check if user already has a profile
        if hasattr(request.user, 'profile'):
            response = {
                "status": 400,
                "success": False,
                "message": "Profile already exists for this user.",
                "data": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        # Create profile for the authenticated user
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Link profile to the authenticated user
            response = {
                "status": 201,
                "success": True,
                "message": "Profile created successfully.",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            "status": 400,
            "success": False,
            "message": "Failed to create profile.",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():  # Added proper validation check
            serializer.save()
            response = {
                "status": 200,
                "success": True,
                "message": "Profile updated successfully.",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        
        # Error handling for invalid data
        response = {
            "status": 400,
            "success": False,
            "message": "Failed to update profile.",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            profile.delete()
            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Profile deleted successfully",
            }
            return Response(response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Profile not found",
            }, status=status.HTTP_404_NOT_FOUND)

