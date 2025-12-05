import traceback
from django.utils.timesince import timesince
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.throttling import UserRateThrottle
from rest_framework import status
from django.db import transaction
# from apps.home.models import SearchTag
from scripts.search_bar import search_bar
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.contrib.contenttypes.models import ContentType
from collections import defaultdict

from .utils import SearchGenThrottle


from .models import (
    Category,
    Subcategory,
    Search,
    UpdateMe,
    Bookmark,
    Preference,
    Trending,
    Recommendation,
    SearchHistory,
)
from apps.community_hubs.models import Post
from apps.users.models import User
from apps.profiles.models import Feedback
from .serializers import (
    CategorySerializer,
    SubcategorySerializer,
    UserSerializer,
    FeedbackSerializer,
    RecommendationSerializer,
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
        response = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Categories fetched successfully",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


class SubcategoryListAPIView(APIView):
    def get(self, request):
        subcategories = Subcategory.objects.all()
        serializer = SubcategorySerializer(subcategories, many=True)
        return Response(serializer.data)

class UserDetailAPIView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
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
            trending_now = Trending.objects.filter(id=pk, is_active=True).select_related("category", "subcategory").first()

            if trending_now:
                obj = {
                    "id": trending_now.id,
                    "topic": trending_now.topic,
                    "category": trending_now.category.category_name,
                    "subcategory": trending_now.subcategory.subcategory_name,
                    "description": trending_now.description,
                    "why_trending": trending_now.why_trending,
                    "key_points": trending_now.key_points,
                    "outlook": trending_now.outlook,
                    "picture_url": trending_now.picture_url,
                    "created_at": trending_now.created_at,
                    "timesince": timesince(trending_now.created_at),
                }
                response = {"code": status.HTTP_200_OK, "success": True, "data": obj}
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "code": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": "Trending news not found",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            # check query params for all
            # check if queryparams all is to true
            if request.query_params.get("all") == "true":
                trending_now = Trending.objects.filter(is_active=True).select_related("category", "subcategory").order_by("-created_at")
            else:
                trending_now = Trending.objects.filter(is_active=True).select_related(
                    "category", "subcategory"
                ).order_by("-created_at")[:8]
        data = []
        for trendig in trending_now:
            obj = {
                "id": trendig.id,
                "topic": trendig.topic,
                "category": trendig.category.category_name,
                "subcategory": trendig.subcategory.subcategory_name,
                "description": trendig.description,
                "why_trending": trendig.why_trending,
                "key_points": trendig.key_points,
                "outlook": trendig.outlook,
                "picture_url": trendig.picture_url,
                "created_at": trendig.created_at,
                "timesince": timesince(trendig.created_at),
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
                "topic": update_me.topic,
                "short_info": update_me.short_info,
                "reference_url": update_me.reference_url,
                "background_story": update_me.background_story,
                "picture_url": update_me.picture_url,
                "created_at": update_me.created_at,
                "timesince": timesince(update_me.created_at),
            }
            response = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "UpdateMe fetched successfully",
                "data": data,
            }
            return Response(response, status=status.HTTP_200_OK)

        user = request.user
        if not user.is_active:
            return Response(
                {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "success": False,
                    "messages": "User not found or account is not activate",
                    
                }
            )
        sub_ctg = user.preferences.category.all()

        # Get top 3 static news (most recent)
        update_me_static3 = list(
            UpdateMe.objects.filter(is_archive=False, is_top3=True, is_active=True).order_by("-created_at")[:3]
        )

        # Prepare list of top3 IDs to exclude in next query
        top3_ids = [x.id for x in update_me_static3]

        # Get 2 random changable items matching user preference, excluding the top 3
        update_for_me = list(
            UpdateMe.objects.filter(category__in=sub_ctg, is_archive=False, is_active=True)
            .exclude(id__in=top3_ids)
            .select_related("category", "subcategory")
            .order_by("?")[:2]
        )

        # Merge the results
        update_me = update_me_static3 + update_for_me

        # Collect serialized data
        data = []
        for update in update_me:
            obj = {
                "id": update.id,
                "category": update.category.category_name if update.category else None,
                "subcategory": (
                    update.subcategory.subcategory_name if update.subcategory else None
                ),
                "topic": update.topic,
                "short_info": update.short_info,
                "reference_url": update.reference_url,
                "background_story": update.background_story,
                "picture_url": update.picture_url,
                "created_at": update.created_at,
                "timesince": timesince(update.created_at),
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
        category = user.preferences.category.all().values_list("id", flat=True)
        if pk:
            recommendation = get_object_or_404(Recommendation, pk=pk)
            serializer = RecommendationSerializer(recommendation)
            response = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Recommendation fetched successfully",
                "data": serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)

        # check query params
        if request.query_params.get("all") == "true":
            recommendations = (
                Recommendation.objects.filter(category__in=category, is_active=True)
                .select_related("category", "subcategory")
                .order_by("-created_at")
            )
        else:
            recommendations = (
                Recommendation.objects.filter(category__id__in=category, is_active=True)
                .select_related("category", "subcategory")
                .order_by("-created_at")[:4]
            )
            print("recommendations:", recommendations)
        serializer = RecommendationSerializer(recommendations, many=True)
        response = {
            "code": status.HTTP_200_OK,
            "success": True,
            "message": "Recommendations fetched successfully",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


class PreferenceAPI(APIView):
    '''
    GET: FETCH ALL PREFERENCES ITEM FROM CATEGORY AND SUBCATEGORY
    POST: SET USER PREFERENCES
    '''
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.prefetch_related("subcategories").filter(is_active=True, is_main=True)
        serializer = CategorySerializer(categories, many=True)
        response_data = {
            "code": status.HTTP_200_OK,
            "success": True,
            "message": "Preferences fetched successfully",
            "data": serializer.data
            
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        user = request.user
        try:
            user = User.objects.get(id=user.id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # get or create preference object
        preference, created = Preference.objects.get_or_create(user=user)

        subcategory_list = []
        for sub in data["subcategories"]:
            subcategory = Subcategory.objects.get(id=sub)
            subcategory_list.append(subcategory)
        
        # set category of the subcategory 
        category_list = []
        for sub in subcategory_list:
            category = Category.objects.get(id=sub.category_id)
            category_list.append(category)
        preference.subcategory.set(subcategory_list)
        preference.category.set(category_list)
        preference.save()


        return Response(
            {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Preferences saved successfully",
            }
        )


class BookmarkAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        user = request.user
        data = request.data

        try:
            content_type = ContentType.objects.get(model=data["obj_type"])
            model_class = content_type.model_class()
            # obj = model_class.objects.get(pk=data["obj_id"])
        except ContentType.DoesNotExist:
            raise ValidationError("Invalid content_type")
        except model_class.DoesNotExist:
            raise ValidationError("Invalid object_id")

        bookmark, created = Bookmark.objects.get_or_create(
            user=user, content_type=content_type, object_id=data["obj_id"]
        )
        if created:
            response_data = {
                "code": status.HTTP_201_CREATED,
                "success": True,
                "message": "Bookmark created successfully",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            # remove from bookmark
            bookmark.delete()
            response_data = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Bookmark Removed Successfully",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user

        # Collect bookmarks in one query (with content type)
        bookmarks = user.bookmark_set.select_related("content_type").all()

        # Group object IDs by model type
        ids_by_model = defaultdict(list)
        for bm in bookmarks:
            ids_by_model[bm.content_type.model].append(bm.object_id)

        # Bulk fetch all objects grouped by type
        trendings = {
            obj.id: obj
            for obj in Trending.objects.filter(id__in=ids_by_model.get("trending", []))
            .select_related("category", "subcategory")
        }
        posts = {
            obj.id: obj
            for obj in Post.objects.filter(id__in=ids_by_model.get("post", []))
            .select_related("category")
        }
        recommendations = {
            obj.id: obj
            for obj in Recommendation.objects.filter(id__in=ids_by_model.get("recommendation", []))
            .select_related("category")
        }
        updateme_objs = {
            obj.id: obj
            for obj in UpdateMe.objects.filter(id__in=ids_by_model.get("updateme", []))
            .select_related("category", "subcategory")
        }
        search_objs = {
            obj.id: obj
            for obj in Search.objects.filter(id__in=ids_by_model.get("search", []))
            .select_related("category", "subcategory")
        }

        # Initialize response lists
        trending_data, community_post, recommendation_data, updateme_data, search_bar = [], [], [], [], []

        base_url = request.build_absolute_uri("/")

        # Preserve the same loop structure to maintain your response format
        for bookmark in bookmarks:
            model = bookmark.content_type.model
            obj_id = bookmark.object_id

            if model == "trending" and obj_id in trendings:
                obj = trendings[obj_id]
                trending_data.append(
                    {
                        "id": obj.id,
                        "category": obj.category.category_name,
                        "subcategory": obj.subcategory.subcategory_name,
                        "picture_url": obj.picture_url,
                        "created_at": obj.created_at,
                        "timesince": timesince(obj.created_at),
                        "details_url": f"{base_url}api/home/trending-now/{obj.id}/",
                    }
                )

            elif model == "post" and obj_id in posts:
                obj = posts[obj_id]
                community_post.append(
                    {
                        "id": obj.id,
                        "category": (
                            obj.category.category_name if obj.category else None
                        ),
                        "title": obj.title,
                        "image_url": obj.image.url if obj.image else None,
                        "created_at": obj.created_at,
                        "timesince": timesince(obj.created_at),
                    }
                )

            elif model == "recommendation" and obj_id in recommendations:
                obj = recommendations[obj_id]
                recommendation_data.append(
                    {
                        "id": obj.id,
                        "category": obj.category.category_name,
                        "topic": obj.topic,
                        "headline": obj.headline,
                        "picture_url": obj.picture_url,
                        "created_at": obj.created_at,
                        "timesince": timesince(obj.created_at),
                    }
                )

            elif model == "updateme" and obj_id in updateme_objs:
                obj = updateme_objs[obj_id]
                updateme_data.append(
                    {
                        "id": obj.id,
                        "category": obj.category.category_name,
                        "subcategory": obj.subcategory.subcategory_name,
                        "topic": obj.topic,
                        "picture_url": obj.picture_url,
                        "created_at": obj.created_at,
                        "timesince": timesince(obj.created_at),
                    }
                )
            elif model == "search" and obj_id in search_objs:
                obj = search_objs[obj_id]
                search_bar.append(
                    {
                        "id": obj.id,
                        "category": obj.category.category_name,
                        "subcategory": obj.subcategory.subcategory_name,
                        "topic": obj.topic,
                        "general_facts": obj.general_fact,
                        "news": obj.news,
                        "interesting_trivia": obj.interesting_trivia,
                        "opinions": obj.opinion,
                        "questions": obj.question,
                        "further_key_words": obj.further_key_words,
                        "search_term": obj.search_term,
                        "created_at": obj.created_at,
                        "timesince": timesince(obj.created_at),
                    }
                )

        response_data = {
            "code": status.HTTP_200_OK,
            "success": True,
            "message": "Bookmarks fetched successfully",
            "data": {
                "trending": trending_data,
                "community_post": community_post,
                "recommendation": recommendation_data,
                "updateme": updateme_data,
                "search_bar": search_bar,
            },
        }
        return Response(response_data, status=status.HTTP_200_OK)


class SearchAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [SearchGenThrottle]

    def post(self, request):
        data = request.data
        search_term = data.get("search_term", "").lower()

        if not search_term:
            return Response(
                {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "success": False,
                    "message": "Search term is required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save search history if not already saved
        if not SearchHistory.objects.filter(search_term__iexact=search_term).exists():
            try:
                SearchHistory.objects.create(search_term=search_term, user=request.user)
            except Exception as e:
                print(f"Error saving search history: {e}")
                pass

        previous_search = Search.objects.filter(
            search_term__iexact=search_term
        ).values("search_term", "id").first()
        if previous_search:
            search_item = Search.objects.get(id=previous_search["id"])
            print("get from previous search")
            return Response(
                {
                    "code": status.HTTP_200_OK,
                    "success": True,
                    "message": "News fetched successfully",
                    "data": model_to_dict(search_item),
                },
                status=status.HTTP_200_OK,
            )
        else:
            pass

        try:
            _, get_news_data = search_bar(search_term, allow_options=False)

            # Validate keys
            required_keys = [
                "category",
                "subcatetgory",  # typo from script - subcatetgory
                "topic",
                "general_facts",
                "news",
                "interesting_trivia",
                "opinions",
                "questions",
                "further_key_words",
            ]
            for key in required_keys:
                if key not in get_news_data.keys():
                    raise ValueError(f"Missing key in get_news_data: '{key}'")

            category_data = get_news_data["category"]
            subcategory_data = get_news_data["subcatetgory"]
            topic_data = get_news_data["topic"]

            category_name = category_data.get("categorie_name")
            subcategory_name = subcategory_data.get(
                "subcatetgory_name"
            )  # typo from script - subcatetgory_name
            topic_name = topic_data.get("name")

            if not category_name or not subcategory_name or not topic_name:
                raise ValueError("Missing category/subcategory/topic names")

            category, _ = Category.objects.get_or_create(
                category_name=category_name
            )
            subcategory, _ = Subcategory.objects.get_or_create(
                category=category,
                subcategory_name=subcategory_name
            )

            # Create Search (News) object
            search_news = Search.objects.create(
                topic=topic_name,
                category=category,
                subcategory=subcategory,
                general_fact=get_news_data["general_facts"],
                news=get_news_data["news"],
                interesting_trivia=get_news_data["interesting_trivia"],
                opinion=get_news_data["opinions"],
                question=get_news_data["questions"],
                further_key_words=get_news_data["further_key_words"],
                search_term=search_term,
            )

            return Response(
                {
                    "code": status.HTTP_200_OK,
                    "success": True,
                    "message": "News fetched successfully",
                    "data": model_to_dict(search_news),
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            print("Error generating news:\n", traceback.format_exc())
            return Response(
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "success": False,
                    "message": f"Error generating news: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SearchHistoryAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        search_history = SearchHistory.objects.filter(user=user)
        data = [
            {"id": history.id, "search_term": history.search_term}
            for history in search_history
        ]
        return Response(
            {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Search history fetched successfully",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk=None):
        user = request.user
        params = request.query_params.get("all")

        if params and params.lower() == "true":
            # Handle deletion of all search history
            if pk is not None:
                return Response(
                    {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "success": False,
                        "message": "Cannot specify 'pk' when deleting all search history",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            deleted_count, _ = SearchHistory.objects.filter(user=user).delete()
            return Response(
                {
                    "code": status.HTTP_200_OK,
                    "success": True,
                    "message": f"Cleared {deleted_count} search history record(s)",
                },
                status=status.HTTP_200_OK,
            )

        # Handle deletion of a specific search history record
        if pk is None:
            return Response(
                {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "success": False,
                    "message": "Missing 'pk' or 'all=true' parameter",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            search_history = SearchHistory.objects.get(user=user, pk=pk) 
            search_history.delete()
            return Response(
                {
                    "code": status.HTTP_200_OK,
                    "success": True,
                    "message": "Search history record deleted successfully",
                },
                status=status.HTTP_200_OK,
            )
        except SearchHistory.DoesNotExist:
            return Response(
                {
                    "code": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": "Search history record not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
