from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType


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
    Bookmark,
    # Preference,
    Trending,
    Recommendation
)
from apps.community_hubs.models import Post
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
    RecommendationSerializer,
    PreferenceSerializer
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


class TrendingNowAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            trending_now = Trending.objects.filter(id=pk).first()
            if trending_now:
                obj = {
                    "id": trending_now.id,
                    "category": trending_now.category.category_name,
                    "subcategory": trending_now.subcategory.subcategory_name,
                    "description": trending_now.description,
                    "why_trending": trending_now.why_trending,
                    "key_points": trending_now.key_points,
                    "outlook": trending_now.outlook,
                    "picture_url": trending_now.picture_url,
                    "created_at": trending_now.created_at,
                }
                response = {"code": status.HTTP_200_OK, "success": True, "data": obj}
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "code": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": "Trending news not found"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            # check query params for all
            # check if queryparams all is to true
            if request.query_params.get("all") == "true":
                trending_now = Trending.objects.all().order_by("-created_at")
            else:
                trending_now = Trending.objects.select_related("category", "subcategory").order_by("-created_at")[:4]
        data = []
        for trendig in trending_now:
            obj = {
                "id": trendig.id,
                "category": trendig.category.category_name,
                "subcategory": trendig.subcategory.subcategory_name,
                "description": trendig.description,
                "why_trending": trendig.why_trending,
                "key_points": trendig.key_points,
                "outlook": trendig.outlook,
                "picture_url": trendig.picture_url,
                "created_at": trendig.created_at,
            }
            data.append(obj)

        response = {"code": status.HTTP_200_OK, "success": True, "data": data}
        return Response(response, status=status.HTTP_200_OK)


class UpdatemeAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):

        if id:
            update_me = get_object_or_404(UpdateMe, pk=id)
            data = {
                "id": update_me.id,
                "category": update_me.category.category_name,
                "subcategory": update_me.subcategory.subcategory_name,
                "topic": update_me.topic.name,
                "short_info": update_me.short_info,
                "reference_url": update_me.reference_url,
                "background_story": update_me.background_story,
                "picture_url": update_me.picture_url,
                "created_at": update_me.created_at,
            }
            response = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "UpdateMe fetched successfully",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)

        user = request.user
        sub_ctg = user.preferences.subcategory.all()
        upate_me_last3 = UpdateMe.objects.order_by("-created_at")[:3]
        update_for_me = UpdateMe.objects.filter(subcategory__in=sub_ctg).select_related("category", "subcategory", "topic").order_by("-created_at")[:2]

        # merge two querysets
        update_me = list(update_for_me) + list(upate_me_last3)

        data = []
        for update in update_me:
            obj = {
                "id": update.id,
                "category": update.category.category_name,
                "subcategory": update.subcategory.subcategory_name,
                "topic": update.topic.name,
                "short_info": update.short_info,
                "reference_url": update.reference_url,
                "background_story": update.background_story,
                "picture_url": update.picture_url,
                "created_at": update.created_at,
            }
            data.append(obj)

        response = {"code": status.HTTP_200_OK, "success": True, "data": data}
        return Response(response, status=status.HTTP_200_OK)


class RecommendationAPI(APIView):
    """
    RESPONSE CONTAINS RECOMMENDATIONS BASED ON USER PREFERENCES (CATEGORY)
    DEFAULT LIMIT IS 4 RECOMMENDATIONS
    IF ALL IS TRUE IN QUERY PARAMS, THEN ALL RECOMMENDATIONS ARE RETURNED
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user
        if pk:
            recommendation = get_object_or_404(Recommendation, pk=pk)
            serializer = RecommendationSerializer(recommendation)
            response = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Recommendation fetched successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

        category = user.preferences.category.all()

        # check query params 
        if request.query_params.get("all") == "true":
            recommendations = Recommendation.objects.filter(category__in=category).select_related("category", "topic").order_by("-created_at")
        else:
            recommendations = Recommendation.objects.filter(category__in=category).select_related("category", "topic").order_by("-created_at")[:4]
        serializer = RecommendationSerializer(recommendations, many=True)
        response = {
            "code": status.HTTP_200_OK,
            "success": True,
            "message": "Recommendations fetched successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class PreferenceAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        subcateories = Subcategory.objects.all()

        response_data = {
            "code": status.HTTP_200_OK,
            "success": True,
            "message": "Preferences fetched successfully",
            "data": {
                "categories": CategorySerializer(categories, many=True).data,
                "subcategories": SubcategorySerializer(subcateories, many=True).data
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PreferenceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Preferences updated successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            raise ValidationError("Invalid data")


class BookmarkAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass

    def get(self, request):
        user = request.user
        bookmarks = user.bookmark_set.all()

        trending_data = []
        community_post = []
        recommendation_data = []
        updateme_data = []

        base_url = request.build_absolute_uri("/")
        print(base_url)

        for bookmark in bookmarks:
            content_type = bookmark.content_type.model
            obj = bookmark.obj

            if isinstance(obj, Trending):
                trending_data.append({
                    "id": obj.id,
                    "category": obj.category.category_name,
                    "subcategory": obj.subcategory.subcategory_name,
                    "picture_url": obj.picture_url,
                    "created_at": obj.created_at,
                    "details_url": base_url + 'api/home/trending-now/' + str(obj.id) + '/'

                })
            elif isinstance(obj, Post):
                community_post.append({
                    "id": obj.id,
                    "category": obj.category.category_name if obj.category else None,
                    "title": obj.title,
                    "image_url": obj.image.url if obj.image else None,
                    "created_at": obj.created_at,
                })
            elif isinstance(obj, Recommendation):
                recommendation_data.append({
                    "id": obj.id,
                    "category": obj.category.category_name,
                    "subcategory": obj.subcategory.subcategory_name if obj.subcategory else None,
                    "topic": obj.topic.name,
                    "headline": obj.headline,
                    "picture_url": obj.picture_url,
                    "created_at": obj.created_at,
                })
            elif isinstance(obj, UpdateMe):
                updateme_data.append({
                    "id": obj.id,
                    "category": obj.category.category_name,
                    "subcategory": obj.subcategory.subcategory_name,
                    "topic": obj.topic.name,
                    "picture_url": obj.picture_url,
                    "created_at": obj.created_at,
                })
            else:
                pass

        response_data = {
            "code": status.HTTP_200_OK,
            "success": True,
            "message": "Bookmarks fetched successfully",
            "data": {
                "trending": trending_data,
                "community_post": community_post,
                "recommendation": recommendation_data,
                "updateme": updateme_data
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

