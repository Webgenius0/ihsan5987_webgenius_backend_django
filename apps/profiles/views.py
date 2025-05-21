from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer, MyPostSerializer, FAQSerializer, FAQCategorySerializer, ContactUsSerializer
from apps.community_hubs.models import Post
from .models import Profile, FAQ, FAQCategory, ContactUs
from django.shortcuts import get_object_or_404
from django.db.models import Q

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
        
        serializer = ProfileSerializer(profile, context={'request' : request})
        response = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Profile retrieved successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    # def post(self, request):
    #     # Check if user already has a profile
    #     if hasattr(request.user, 'profile'):
    #         response = {
    #             "status": 400,
    #             "success": False,
    #             "message": "Profile already exists for this user.",
    #             "data": None
    #         }
    #         return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
    #     # Create profile for the authenticated user
    #     serializer = ProfileSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)  # Link profile to the authenticated user
    #         response = {
    #             "status": 201,
    #             "success": True,
    #             "message": "Profile created successfully.",
    #             "data": serializer.data
    #         }
    #         return Response(response, status=status.HTTP_201_CREATED)
    #     response = {
    #         "status": 400,
    #         "success": False,
    #         "message": "Failed to create profile.",
    #         "data": serializer.errors
    #     }
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
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


class MyPostList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        posts = Post.objects.filter(user=user).order_by('-created_at')
        serializer = MyPostSerializer(posts, many=True)
        response = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Posts retrieved successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class MyPostDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, user=request.user)
        except Post.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Post not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = MyPostSerializer(post, context={'request': request})
        response = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Post retrieved successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, user=request.user)
        except Post.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Post not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = MyPostSerializer(post, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Post updated successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, user=request.user)
        except Post.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Post not found"
            }, status=status.HTTP_404_NOT_FOUND)

        post.delete()
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Post deleted successfully"
        }, status=status.HTTP_200_OK)

    

# FAQ View
class FAQList(APIView):
    def get(self, request):
        category = request.query_params.get('category', None)
        search = request.query_params.get('search', None)
        
        if category:
            faqs = FAQ.objects.filter(category__name=category)
        elif search:
            faqs = FAQ.objects.filter(Q(question__icontains=search) | Q(answer__icontains=search))
        else:
            faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True)
        response = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "FAQs retrieved successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
class FAQCategoryList(APIView):
    def get(self, request):
        categories = FAQCategory.objects.all()
        serializer = FAQCategorySerializer(categories, many=True)
        response = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "FAQ categories retrieved successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
# Contact Us View
class ContactUsList(APIView):
    def get(self, request):
        contacts = ContactUs.objects.all()
        serializer = ContactUsSerializer(contacts, many=True)
        response = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Contact Us links retrieved successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)