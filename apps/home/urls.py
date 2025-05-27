from django.urls import path
from .views import TrendingNewsAPIView, TrendingNewsDetailAPIView, RecommendedTopicsAPIView, RecommendedTopicsDetailsAPIView, SearchResultsAPIView, UpdateMeAPIView, YourNewsAPIView, YourInterestAPIView, UserInterestsAPIView, CommunityHubAPIView

urlpatterns = [
    path('trending_news/', TrendingNewsAPIView.as_view(), name='trending-news'),
    path('trending_news/<int:id>/', TrendingNewsDetailAPIView.as_view(), name='trending-news-id'),
    path('recommended_topics/', RecommendedTopicsAPIView.as_view(), name='recommended-topics'),
    path('recommended_topics/<int:id>/', RecommendedTopicsDetailsAPIView.as_view(), name='recommended-topics-id'),
    path('community_hub/', CommunityHubAPIView.as_view(), name='community-hub'),
    path('search_results/', SearchResultsAPIView.as_view(), name='search-results'),
    path('update_me/', UpdateMeAPIView.as_view(), name='update-me'),
    path('posts/', UpdateMeAPIView.as_view(), name='posts'),
    path('your_news/', YourNewsAPIView.as_view(), name='your-news'),
    path('your_interests/', YourInterestAPIView.as_view(), name='your-interests'),

    path('user_interests/', UserInterestsAPIView.as_view(), name='user-interests'),
]