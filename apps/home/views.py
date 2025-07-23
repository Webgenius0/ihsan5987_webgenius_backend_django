from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import (
    Response as ResponseModel,
    Topic,
    Category,
    Subcategory,
    GeneralFact,
    News,
    InterestingTrivia,
    Opinion,
    Question,
    Search,
    UpdateMe,
    Preference
)
from apps.users.models import User
from apps.profiles.models import Feedback
from .serializers import (
    ResponseSerializer,
    TopicSerializer,
    CategorySerializer,
    SubcategorySerializer,
    GeneralFactSerializer,
    NewsSerializer,
    InterestingTriviaSerializer,
    OpinionSerializer,
    QuestionSerializer,
    UserSerializer,
    SearchSerializer,
    FeedbackSerializer,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# Generic pattern for List + Detail APIViews:
class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetailAPIView(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class SubcategoryListAPIView(APIView):
    def get(self, request):
        subcategories = Subcategory.objects.all()
        serializer = SubcategorySerializer(subcategories, many=True)
        return Response(serializer.data)


class SubcategoryDetailAPIView(APIView):
    def get(self, request, pk):
        subcategory = get_object_or_404(Subcategory, pk=pk)
        serializer = SubcategorySerializer(subcategory)
        return Response(serializer.data)


class TopicListAPIView(APIView):
    def get(self, request):
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)


class TopicDetailAPIView(APIView):
    def get(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)
        serializer = TopicSerializer(topic)
        return Response(serializer.data)


class GeneralFactListAPIView(APIView):
    def get(self, request):
        facts = GeneralFact.objects.all()
        serializer = GeneralFactSerializer(facts, many=True)
        return Response(serializer.data)


class GeneralFactDetailAPIView(APIView):
    def get(self, request, pk):
        fact = get_object_or_404(GeneralFact, pk=pk)
        serializer = GeneralFactSerializer(fact)
        return Response(serializer.data)


class NewsListAPIView(APIView):
    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)


class NewsDetailAPIView(APIView):
    def get(self, request, pk):
        news_item = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(news_item)
        return Response(serializer.data)


class InterestingTriviaListAPIView(APIView):
    def get(self, request):
        trivia = InterestingTrivia.objects.all()
        serializer = InterestingTriviaSerializer(trivia, many=True)
        return Response(serializer.data)


class InterestingTriviaDetailAPIView(APIView):
    def get(self, request, pk):
        trivia = get_object_or_404(InterestingTrivia, pk=pk)
        serializer = InterestingTriviaSerializer(trivia)
        return Response(serializer.data)


class OpinionListAPIView(APIView):
    def get(self, request):
        opinions = Opinion.objects.all()
        serializer = OpinionSerializer(opinions, many=True)
        return Response(serializer.data)


class OpinionDetailAPIView(APIView):
    def get(self, request, pk):
        opinion = get_object_or_404(Opinion, pk=pk)
        serializer = OpinionSerializer(opinion)
        return Response(serializer.data)


class QuestionListAPIView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class QuestionDetailAPIView(APIView):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)


class UserDetailAPIView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class ResponseListAPIView(APIView, StandardResultsSetPagination):
    def get(self, request):
        responses = ResponseModel.objects.all()
        category_id = request.query_params.get("category_id")
        topic_id = request.query_params.get("topic_id")

        if category_id:
            responses = responses.filter(category_id=category_id)
        if topic_id:
            responses = responses.filter(topic_id=topic_id)

        results = self.paginate_queryset(responses, request, view=self)
        serializer = ResponseSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class ResponseDetailAPIView(APIView):
    def get(self, request, pk):
        response = get_object_or_404(ResponseModel, pk=pk)
        serializer = ResponseSerializer(response)
        return Response(serializer.data)


class SearchListAPIView(APIView, StandardResultsSetPagination):
    def get(self, request):
        searches = Search.objects.all()
        user_id = request.query_params.get("user_id")
        if user_id:
            searches = searches.filter(user_id=user_id)
        results = self.paginate_queryset(searches, request, view=self)
        serializer = SearchSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class SearchDetailAPIView(APIView):
    def get(self, request, pk):
        search = get_object_or_404(Search, pk=pk)
        serializer = SearchSerializer(search)
        return Response(serializer.data)


class FeedbackListAPIView(APIView, StandardResultsSetPagination):
    def get(self, request):
        feedbacks = Feedback.objects.all()
        user_id = request.query_params.get("user_id")
        if user_id:
            feedbacks = feedbacks.filter(user_id=user_id)
        results = self.paginate_queryset(feedbacks, request, view=self)
        serializer = FeedbackSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class FeedbackDetailAPIView(APIView):
    def get(self, request, pk):
        feedback = get_object_or_404(Feedback, pk=pk)
        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data)

# Views for Home Page


class UpdateMeAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_preferences = Preference.objects.filter(user=user).values_list('category__category_name', flat=True)
        print("user preferences", user_preferences)
        # get letest 3 updateme objects
        updateme_last3 = UpdateMe.objects.order_by('-created_at')[:3]
        print("updateme_last3", updateme_last3)
        updateme_preferences = UpdateMe.objects.filter(subcategory__subcategory_name__in=user_preferences).order_by('-created_at').exclude(id__in=[um.id for um in updateme_last3])[:2]
        print("updateme_preferences", updateme_preferences)

        response_data = {
            "code": 200,
            "message": "Success",
        }
        return Response(response_data, status=status.HTTP_200_OK)
