from django.urls import path
from .views import (
    CategoryListAPIView, CategoryDetailAPIView,
    SubcategoryListAPIView, SubcategoryDetailAPIView,
    TopicListAPIView, TopicDetailAPIView,
    GeneralFactListAPIView, GeneralFactDetailAPIView,
    NewsListAPIView, NewsDetailAPIView,
    InterestingTriviaListAPIView, InterestingTriviaDetailAPIView,
    OpinionListAPIView, OpinionDetailAPIView,
    QuestionListAPIView, QuestionDetailAPIView,
    UserDetailAPIView,
    ResponseListAPIView, ResponseDetailAPIView,
    SearchListAPIView, SearchDetailAPIView,
    FeedbackListAPIView, FeedbackDetailAPIView,
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),

    # Subcategories
    path('subcategories/', SubcategoryListAPIView.as_view(), name='subcategory-list'),
    path('subcategories/<int:pk>/', SubcategoryDetailAPIView.as_view(), name='subcategory-detail'),

    # Topics
    path('topics/', TopicListAPIView.as_view(), name='topic-list'),
    path('topics/<int:pk>/', TopicDetailAPIView.as_view(), name='topic-detail'),

    # General Facts
    path('general-facts/', GeneralFactListAPIView.as_view(), name='generalfact-list'),
    path('general-facts/<int:pk>/', GeneralFactDetailAPIView.as_view(), name='generalfact-detail'),

    # News
    path('news/', NewsListAPIView.as_view(), name='news-list'),
    path('news/<int:pk>/', NewsDetailAPIView.as_view(), name='news-detail'),

    # Interesting Trivia
    path('trivia/', InterestingTriviaListAPIView.as_view(), name='trivia-list'),
    path('trivia/<int:pk>/', InterestingTriviaDetailAPIView.as_view(), name='trivia-detail'),

    # Opinions
    path('opinions/', OpinionListAPIView.as_view(), name='opinion-list'),
    path('opinions/<int:pk>/', OpinionDetailAPIView.as_view(), name='opinion-detail'),

    # Questions
    path('questions/', QuestionListAPIView.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetailAPIView.as_view(), name='question-detail'),

    # Users
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),

    # Responses
    path('responses/', ResponseListAPIView.as_view(), name='response-list'),
    path('responses/<int:pk>/', ResponseDetailAPIView.as_view(), name='response-detail'),

    # Searches
    path('searches/', SearchListAPIView.as_view(), name='search-list'),
    path('searches/<int:pk>/', SearchDetailAPIView.as_view(), name='search-detail'),

    # Feedbacks
    path('feedbacks/', FeedbackListAPIView.as_view(), name='feedback-list'),
    path('feedbacks/<int:pk>/', FeedbackDetailAPIView.as_view(), name='feedback-detail'),
]
