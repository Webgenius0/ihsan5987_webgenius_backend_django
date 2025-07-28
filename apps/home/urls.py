from django.urls import path
from apps.community_hubs.views import PostList
from . import views

urlpatterns = [
    # Categories
    path("categories/", views.CategoryListAPIView.as_view(), name="category-list"),
    path(
        "categories/<int:pk>/", views.CategoryDetailAPIView.as_view(), name="category-detail"
    ),
    # Subcategories
    path("subcategories/", views.SubcategoryListAPIView.as_view(), name="subcategory-list"),
    path(
        "subcategories/<int:pk>/",
        views.SubcategoryDetailAPIView.as_view(),
        name="subcategory-detail",
    ),
    # Topics
    path("topics/", views.TopicListAPIView.as_view(), name="topic-list"),
    path("topics/<int:pk>/", views.TopicDetailAPIView.as_view(), name="topic-detail"),
    # General Facts
    path("general-facts/", views.GeneralFactListAPIView.as_view(), name="generalfact-list"),
    path(
        "general-facts/<int:pk>/",
        views.GeneralFactDetailAPIView.as_view(),
        name="generalfact-detail",
    ),
    # News
    path("news/", views.NewsListAPIView.as_view(), name="news-list"),
    path("news/<int:pk>/", views.NewsDetailAPIView.as_view(), name="news-detail"),
    # Interesting Trivia
    path("trivia/", views.InterestingTriviaListAPIView.as_view(), name="trivia-list"),
    path(
        "trivia/<int:pk>/",
        views.InterestingTriviaDetailAPIView.as_view(),
        name="trivia-detail",
    ),
    # Opinions
    path("opinions/", views.OpinionListAPIView.as_view(), name="opinion-list"),
    path("opinions/<int:pk>/", views.OpinionDetailAPIView.as_view(), name="opinion-detail"),
    # Questions
    path("questions/", views.QuestionListAPIView.as_view(), name="question-list"),
    path(
        "questions/<int:pk>/", views.QuestionDetailAPIView.as_view(), name="question-detail"
    ),
    # Users
    path("users/<int:pk>/", views.UserDetailAPIView.as_view(), name="user-detail"),
    # Responses
    path("responses/", views.ResponseListAPIView.as_view(), name="response-list"),
    path(
        "responses/<int:pk>/", views.ResponseDetailAPIView.as_view(), name="response-detail"
    ),
    # Searches
    path("searches/", views.SearchListAPIView.as_view(), name="search-list"),
    path("searches/<int:pk>/", views.SearchDetailAPIView.as_view(), name="search-detail"),
    # Feedbacks
    path("feedbacks/", views.FeedbackListAPIView.as_view(), name="feedback-list"),
    path(
        "feedbacks/<int:pk>/", views.FeedbackDetailAPIView.as_view(), name="feedback-detail"
    ),
    # Community Hubs Post
    path("posts/", PostList.as_view(), name="community-hubs-post"),
    
    # HOME VIEW
    path("update/", views.UpdatemeAPI.as_view(), name="update-me"),
    path("trending-now/", views.TrendingNowAPI.as_view(), name="trending-now"),
    path("trending-now/<int:pk>/", views.TrendingNowAPI.as_view(), name="trending-now-details"),

    path("recommendation-news/", views.RecommendationAPI.as_view(), name="recommendation-news"),
    path("recommendation-news/<int:pk>/", views.RecommendationAPI.as_view(), name="recommendation-news-details"),
]
