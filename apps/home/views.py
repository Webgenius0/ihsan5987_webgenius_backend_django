import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from .models import UserInterests, NewsBookmark, TrendingNews
from apps.users.authentication import CustomJWTAuthentication
from .serializers import UserInterestsSerializer, TrendingNewsSerializer
from .utils import trending_news_store
from apps.community_hubs.models import Post
from apps.community_hubs.serializers import PostlistSerializer
from django.shortcuts import get_object_or_404


# Trending News API
class TrendingNewsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trending_news_store()
        articles = TrendingNews.objects.all().order_by('-published_at')
        serializer = TrendingNewsSerializer(articles, many=True, context={'request': request})
        response_data = {
            'status': status.HTTP_200_OK,
            'success': True,
            'message': 'Trending news fetched successfully',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
# Trending News Detail API
class TrendingNewsDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        article = get_object_or_404(TrendingNews, id=id)
        serializer = TrendingNewsSerializer(
            article,
            context={'request': request}
        )
        return Response({
            'status': status.HTTP_200_OK,
            'success': True,
            'message': 'Trending news detail fetched successfully',
            'data': serializer.data
        })

class BookmarkNewsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, article_id):
        article = get_object_or_404(TrendingNews, id=article_id)
        bookmark, created = NewsBookmark.objects.get_or_create(user=request.user, article=article)
        if created:
            return Response({'success': True, 'message': 'Article bookmarked.'})
        return Response({'success': False, 'message': 'Article already bookmarked.'})

    def delete(self, request, article_id):
        article = get_object_or_404(TrendingNews, id=article_id)
        bookmark = NewsBookmark.objects.filter(user=request.user, article=article).first()
        if bookmark:
            bookmark.delete()
            return Response({'success': True, 'message': 'Bookmark removed.'})
        return Response({'success': False, 'message': 'Bookmark not found.'})
        
#Recommended Topics API
class RecommendedTopicsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        articles = TrendingNews.objects.all().order_by('-published_at')
        serializer = TrendingNewsSerializer(articles, many=True, context={'request': request})
        return Response({
            'status': status.HTTP_200_OK,
            'success': True,
            'message': 'Recommended topics fetched successfully',
            'data': serializer.data
        })
    
#Trending News Detail API
class RecommendedTopicsDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        article = get_object_or_404(TrendingNews, id=id)
        serializer = TrendingNewsSerializer(article, context={'request': request})
        return Response({
            'status': status.HTTP_200_OK,
            'success': True,
            'message': 'Trending news detail fetched successfully',
            'data': serializer.data
        })



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



#User interests API
from rest_framework import generics, permissions, status
from .models import UserInterests, UserPreference, Interest
from .serializers import UserInterestsSerializer, UserPreferenceSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

class UserInterestsView(generics.RetrieveUpdateAPIView):
    """
    GET: Retrieve current user's interests
    PUT/PATCH: Update current user's interests (set list)
    """
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = UserInterestsSerializer

    def get_object(self):
        # Get or create UserInterests for current user
        obj, created = UserInterests.objects.get_or_create(user=self.request.user)
        return obj

    def perform_update(self, serializer):
        # You can add extra logic here if needed
        serializer.save()

class UserPreferencesListView(generics.ListAPIView):
    """
    GET: List user's tracked preferences (clicked interests)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserPreferenceSerializer

    def get_queryset(self):
        return UserPreference.objects.filter(user=self.request.user).order_by('-clicked_at')

class TrackUserPreferenceView(APIView):
    """
    POST: Track a user preference (user clicked an interest)
    Payload: { "interest_id": <id> }
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        interest_id = request.data.get('interest_id')
        if not interest_id:
            return Response({"error": "interest_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            interest = Interest.objects.get(id=interest_id)
        except Interest.DoesNotExist:
            return Response({"error": "Interest not found"}, status=status.HTTP_404_NOT_FOUND)

        obj, created = UserPreference.objects.get_or_create(user=request.user, interest=interest)
        obj.clicked_at = timezone.now()
        obj.save()

        serializer = UserPreferenceSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

