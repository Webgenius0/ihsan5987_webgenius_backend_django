from django.urls import path
from apps.community_hubs.views import PostList
from . import views

urlpatterns = [
    # Categories
    path("categories/", views.CategoryListAPIView.as_view(), name="category-list"),
    path("subcategories/", views.SubcategoryListAPIView.as_view(), name="subcategory-list"),

    # Users
    path("users/<int:pk>/", views.UserDetailAPIView.as_view(), name="user-detail"),
    # Responses

    # Feedbacks
    path("feedbacks/", views.FeedbackListAPIView.as_view(), name="feedback-list"),
    path(
        "feedbacks/<int:pk>/", views.FeedbackDetailAPIView.as_view(), name="feedback-detail"
    ),
    # Community Hubs Post
    path("posts/", PostList.as_view(), name="community-hubs-post"),

    # HOME VIEW
    path("update/", views.UpdatemeAPI.as_view(), name="update-me"),
    path("update/<int:id>/", views.UpdatemeAPI.as_view(), name="update-me"),

    path("trending-now/", views.TrendingNowAPI.as_view()),
    path("trending-now/<int:pk>/", views.TrendingNowAPI.as_view()),
    path("recommendations/", views.RecommendationAPI.as_view()),
    path("recommendations/<int:pk>/", views.RecommendationAPI.as_view()),

    # preferences
    path("preferences/", views.PreferenceAPI.as_view(), name="preference-list"),

    # bookmarks
    path("bookmarks/", views.BookmarkAPIView.as_view(), name="bookmark-list"),

    # search bar
    path("search-bar/", views.SearchAPIView.as_view(), name="search-bar"),
    path("search-history/", views.SearchHistoryAPIView.as_view(), name="search-history"),
    path("search-history/<int:pk>/", views.SearchHistoryAPIView.as_view(), name="search-history"),

]
