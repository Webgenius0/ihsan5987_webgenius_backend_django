import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from .models import Notification, UserInterests
from apps.users.authentication import CustomJWTAuthentication
from .serializers import NotificationSerializer, UserInterestsSerializer
from apps.community_hubs.models import Post
from apps.community_hubs.serializers import PostlistSerializer


#Trending News API
class TrendingNewsAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = ['general', 'world', 'nation', 'business', 'technology', 'entertainment', 'sports', 'science', 'health', 'politics']
    
        aggregated_articles = []

        for category in categories:
            params = {
                'token': settings.GNEWS_API_KEY,
                'lang': 'en',
                'country': 'us',
                'max': 10,  
                'q': category  
            }

            response = requests.get("https://gnews.io/api/v4/top-headlines", params=params)

            if response.status_code == 200:
                articles = response.json().get('articles', [])
                for article in articles:
                    aggregated_articles.append({
                        'title': article.get('title'),
                        'description': article.get('description'),
                        'content': article.get('content'),
                        'url': article.get('url'),
                        'image': article.get('image'),
                        'publishedAt': article.get('publishedAt'),
                        'source': {
                            'name': article.get('source', {}).get('name'),
                            'url': article.get('source', {}).get('url'),
                        },
                        'category': category  # manually tagged category
                    })
        response_data = {
            'status': status.HTTP_200_OK,
            'success': True,
            'message': 'Trending news fetched successfully',
            'data': aggregated_articles
        } 
        return Response(response_data, status=status.HTTP_200_OK)
        
#Recommended Topics API
class RecommendedTopicsAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = ['general', 'world', 'nation', 'business', 'technology', 'entertainment', 'sports', 'science', 'health', 'politics']
    
        recommendations = []

        for category in categories:
            params = {
                'token': settings.GNEWS_API_KEY,
                'lang': 'en',
                'country': 'us',
                'max': 10,  
                'q': category  
            }

            response = requests.get("https://gnews.io/api/v4/search", params=params)

            if response.status_code == 200:
                articles = response.json().get('articles', [])
                for article in articles:
                    recommendations.append({
                        'title': article.get('title'),
                        'description': article.get('description'),
                        'content': article.get('content'),
                        'url': article.get('url'),
                        'image': article.get('image'),
                        'publishedAt': article.get('publishedAt'),
                        'source': {
                            'name': article.get('source', {}).get('name'),
                            'url': article.get('source', {}).get('url'),
                        },
                        'category': category  # manually tagged category
                    })
        response_data = {
            'status': status.HTTP_200_OK,
            'success': True,
            'message': 'Recommended topics fetched successfully',
            'data': recommendations
        } 
        return Response(response_data, status=status.HTTP_200_OK)

#Community Hub API
class CommunityHubAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        posts = Post.objects.all().order_by("-created_at")

        serializer = PostlistSerializer(posts, many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Posts fetched successfully",
            "data": serializer.data
        })

#Search News API
class SearchResultsAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({"error": "Query parameter 'q' is required"}, status=400)

        url = "https://gnews.io/api/v4/search"
        params = {
            'q': query,
            'lang': 'en',
            'max': 10,
            'token': settings.GNEWS_API_KEY
        }
        res = requests.get(url, params=params)
        if res.status_code == 200:
            response_data = {
                'status': status.HTTP_200_OK,
                'success': True,
                'message': 'Search results fetched successfully',
                'data': res.json().get('articles', [])
            } 
            return Response(response_data, status = status.HTTP_200_OK)
        else:
            response_data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'success': False,
                'message': 'Search failed',
                'errors': res.json()
            } 
            return Response(response_data, status = status.HTTP_400_BAD_REQUEST)

#Update Me API
class UpdateMeAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = ['general', 'world', 'nation', 'business', 'technology', 'entertainment', 'sports', 'science', 'health', 'politics']
    
        update = []

        for category in categories:
            params = {
                'token': settings.GNEWS_API_KEY,
                'lang': 'en',
                'country': 'us',
                'max': 10,  
                'q': category  
            }

            response = requests.get("https://gnews.io/api/v4/search", params=params)

            if response.status_code == 200:
                articles = response.json().get('articles', [])
                for article in articles:
                    update.append({
                        'title': article.get('title'),
                        'description': article.get('description'),
                        'content': article.get('content'),
                        'url': article.get('url'),
                        'image': article.get('image'),
                        'publishedAt': article.get('publishedAt'),
                        'source': {
                            'name': article.get('source', {}).get('name'),
                            'url': article.get('source', {}).get('url'),
                        },
                        'category': category  # manually tagged category
                    })
        response_data = {
            'status': status.HTTP_200_OK,
            'success': True,
            'message': 'Update news fetched successfully',
            'data': update
        } 
        return Response(response_data, status=status.HTTP_200_OK)

#Posts View API   
class PostsAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get('q')
        
        if query:
            # Use search endpoint when query is present
            url = "https://gnews.io/api/v4/search"
            params = {
                'q': query,
                'token': settings.GNEWS_API_KEY,
                'lang': 'en',
                'max': 10
            }
        else:
            # Use top-headlines endpoint when query is not present
            url = "https://gnews.io/api/v4/top-headlines"
            params = {
                'token': settings.GNEWS_API_KEY,
                'lang': 'en',
                'country': 'us',
                'max': 10
            }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            response_data = {
                'status': status.HTTP_200_OK,
                'success': True,
                'message': 'Posts fetched successfully',
                'data': response.json().get('articles', [])
            }
            return Response(response_data, status=status.HTTP_200_OK)
        response_data = {
            'status': status.HTTP_400_BAD_REQUEST,
            'success': False,
            'message': 'Failed to fetch posts',
            'errors': response.json()
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

#Your News API
class YourNewsAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        url = "https://gnews.io/api/v4/top-headlines"
        params = {
            'token': settings.GNEWS_API_KEY,
            'lang': 'en',
            'country': 'us',
            'max': 10
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            response_data = {
                'status': status.HTTP_200_OK,
                'success': True,
                'message': 'Your news fetched successfully',
                'data': response.json().get('articles', [])
            }
            return Response(response_data, status=status.HTTP_200_OK)
        response_data = {
            'status': status.HTTP_400_BAD_REQUEST,
            'success': False,
            'message': 'Failed to fetch your news',
            'errors': response.json()
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

#Your Interests API
class YourInterestAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        interests = request.GET.getlist('topics')  # list of interests

        if not interests:
            return Response({'error': 'Please provide at least one topic using ?topics=topic1&topics=topic2'})

        all_articles = []
        for topic in interests:
            url = "https://gnews.io/api/v4/search"
            params = {
                'q': topic,
                'token': settings.GNEWS_API_KEY,
                'lang': 'en',
                'max': 3  # limit per topic
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                all_articles.extend(response.json().get('articles', []))
                response_data = {
                    'status': status.HTTP_200_OK,
                    'success': True,
                    'message': 'Your interests fetched successfully',
                    'data': all_articles
                }
                return Response(response_data, status=status.HTTP_200_OK)
            response_data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'success': False,
                'message': 'Failed to fetch your interests',
                'errors': response.json()
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    

#General Notification API
class GeneralNotificationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         general_notifications = Notification.objects.filter(user=user, notif_type='general')
#         serializer = NotificationSerializer(general_notifications, many=True)
#         response_data = {
#             'status': status.HTTP_200_OK,
#             'success': True,
#             'message': 'General notifications fetched successfully',
#             'data': serializer.data
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

#System Notification API
class SystemNotificationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         system_notifications = Notification.objects.filter(user=user, notif_type='system')
#         serializer = NotificationSerializer(system_notifications, many=True)
#         response_data = {
#             'status': status.HTTP_200_OK,
#             'success': True,
#             'message': 'System notifications fetched successfully',
#             'data': serializer.data
#         }
#         return Response(response_data, status=status.HTTP_200_OK)


#User interests API
class UserInterestsAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve current user's interests
        try:
            user_interests = UserInterests.objects.get(user=request.user)
        except UserInterests.DoesNotExist:
            return Response({'detail': 'No interests found for user.'}, status=404)
        
        serializer = UserInterestsSerializer(user_interests)
        return Response(serializer.data)

    def post(self, request):
        # Create or update the interests
        try:
            user_interests = UserInterests.objects.get(user=request.user)
            serializer = UserInterestsSerializer(user_interests, data=request.data, context={'request': request})
        except UserInterests.DoesNotExist:
            serializer = UserInterestsSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
