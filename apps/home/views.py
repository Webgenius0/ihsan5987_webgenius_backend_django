import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer


#Trending News API
class TrendingNewsAPIView(APIView):
    def get(self, request):
        url = "https://gnews.io/api/v4/top-headlines"
        params = {
            'token': settings.GNEWS_API_KEY,  # <-- Ensure this is set
            'lang': 'en',
            'country': 'us',
            'max': 10
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            response_data = {
                'status': status.HTTP_200_OK,
                'success': True,
                'message': 'Trending news fetched successfully',
                'data': data.get('articles', [])
            } 
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'success': False,
                'message': 'Failed to fetch news',
                'errors': response.json()
            } 
            return Response(response_data, status =status.HTTP_400_BAD_REQUEST)
        
#Recommended Topics API
class RecommendedTopicsAPIView(APIView):
    def get(self, request):
        topics = [
            "technology", "sports", "business", "entertainment",
            "science", "health", "world", "politics"
        ]

        base_url = "https://gnews.io/api/v4/search"
        token = settings.GNEWS_API_KEY
        recommendations = []

        for topic in topics:
            params = {
                'q': topic,
                'lang': 'en',
                'max': 1,
                'token': token
            }
            res = requests.get(base_url, params=params)
            if res.status_code == 200:
                articles = res.json().get('articles', [])
                if articles:
                    recommendations.append({
                        'topic': topic,
                        'article': articles[0]
                    })
        response_data = {
            'status': status.HTTP_200_OK,
            'success': True,
            'message': 'Recommended topics fetched successfully',
            'data': recommendations
        } 
        return Response(response_data, status = status.HTTP_200_OK)

#Search News API
class SearchResultsAPIView(APIView):
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
    def get(self, request):
        topic = request.query_params.get('q')  # Optional query
        now = datetime.utcnow()
        past = now - timedelta(hours=6)

        if topic:
            # If a topic is provided, search for related news
            url = "https://gnews.io/api/v4/search"
            params = {
                'q': topic,
                'lang': 'en',
                'max': 10,
                'from': past.isoformat() + 'Z',
                'to': now.isoformat() + 'Z',
                'token': settings.GNEWS_API_KEY
            }
        else:
            # No topic? Show general recent headlines
            url = "https://gnews.io/api/v4/top-headlines"
            params = {
                'lang': 'en',
                'country': 'us',  # You can change or customize per user
                'max': 10,
                'token': settings.GNEWS_API_KEY
            }

        res = requests.get(url, params=params)
        if res.status_code == 200:
            response_data = {
                'status': status.HTTP_200_OK,
                'success': True,
                'message': 'Update news fetched successfully',
                'data': res.json().get('articles', [])
            }
            return Response(response_data, status=status.HTTP_200_OK)
        response_data = {
            'status': status.HTTP_400_BAD_REQUEST,
            'success': False,
            'message': 'Failed to fetch update news',
            'errors': res.json()
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

#Posts View API   
class PostsAPIView(APIView):
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

    def get(self, request):
        user = request.user
        general_notifications = Notification.objects.filter(user=user, notif_type='general')
        serializer = NotificationSerializer(general_notifications, many=True)
        response_data = {
            'status': status.HTTP_200_OK,
            'success': True,
            'message': 'General notifications fetched successfully',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

#System Notification API
class SystemNotificationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        system_notifications = Notification.objects.filter(user=user, notif_type='system')
        serializer = NotificationSerializer(system_notifications, many=True)
        response_data = {
            'status': status.HTTP_200_OK,
            'success': True,
            'message': 'System notifications fetched successfully',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
