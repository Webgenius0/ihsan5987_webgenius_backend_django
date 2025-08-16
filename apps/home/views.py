import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework import status
from django.db import transaction
from apps.home.models import SearchTag, SearchOption
from SmallTalk.search_bar import search_bar
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.contrib.contenttypes.models import ContentType


from .models import (
    Topic,
    Category,
    Subcategory,
    Search,
    UpdateMe,
    Bookmark,
    # Preference,
    Trending,
    Recommendation,
    SearchHistory,
)
from apps.community_hubs.models import Post
from apps.users.models import User
from apps.profiles.models import Feedback
from .serializers import (
    TopicSerializer,
    CategorySerializer,
    SubcategorySerializer,
    UserSerializer,
    FeedbackSerializer,
    RecommendationSerializer,
    PreferenceSerializer,
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
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


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
                    "message": "Trending news not found",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            # check query params for all
            # check if queryparams all is to true
            if request.query_params.get("all") == "true":
                trending_now = Trending.objects.all().order_by("-created_at")
            else:
                trending_now = Trending.objects.select_related(
                    "category", "subcategory"
                ).order_by("-created_at")[:4]
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
                "data": data,
            }
            return Response(response, status=status.HTTP_200_OK)

        user = request.user
        sub_ctg = user.preferences.subcategory.all()
        upate_me_last3 = UpdateMe.objects.order_by("-created_at")[:3]
        update_for_me = (
            UpdateMe.objects.filter(subcategory__in=sub_ctg)
            .select_related("category", "subcategory", "topic")
            .order_by("-created_at")[:2]
        )

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
        category = user.preferences.category.all().values_list("id", flat=True)
        print("user preferences category:", category)
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
                Recommendation.objects.filter(category__in=category)
                .select_related("category", "topic")
                .order_by("-created_at")
            )
        else:
            recommendations = (
                Recommendation.objects.filter(category__id__in=category)
                .select_related("category", "topic")
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
                "subcategories": SubcategorySerializer(subcateories, many=True).data,
            },
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PreferenceSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Preferences updated successfully",
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            raise ValidationError("Invalid data")


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
            response_data = {
                "code": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Bookmark already exists",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

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
            # content_type = bookmark.content_type.model
            obj = bookmark.obj

            if isinstance(obj, Trending):
                trending_data.append(
                    {
                        "id": obj.id,
                        "category": obj.category.category_name,
                        "subcategory": obj.subcategory.subcategory_name,
                        "picture_url": obj.picture_url,
                        "created_at": obj.created_at,
                        "details_url": base_url + "api/home/trending-now/" + str(obj.id) + "/",
                    }
                )
            elif isinstance(obj, Post):
                community_post.append(
                    {
                        "id": obj.id,
                        "category": (
                            obj.category.category_name if obj.category else None
                        ),
                        "title": obj.title,
                        "image_url": obj.image.url if obj.image else None,
                        "created_at": obj.created_at,
                    }
                )
            elif isinstance(obj, Recommendation):
                recommendation_data.append(
                    {
                        "id": obj.id,
                        "category": obj.category.category_name,
                        "subcategory": (
                            obj.subcategory.subcategory_name
                            if obj.subcategory
                            else None
                        ),
                        "topic": obj.topic.name,
                        "headline": obj.headline,
                        "picture_url": obj.picture_url,
                        "created_at": obj.created_at,
                    }
                )
            elif isinstance(obj, UpdateMe):
                updateme_data.append(
                    {
                        "id": obj.id,
                        "category": obj.category.category_name,
                        "subcategory": obj.subcategory.subcategory_name,
                        "topic": obj.topic.name,
                        "picture_url": obj.picture_url,
                        "created_at": obj.created_at,
                    }
                )
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
                "updateme": updateme_data,
            },
        }
        return Response(response_data, status=status.HTTP_200_OK)


# class SearchAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         data = request.data
#         get_news = data.get("get_news", False)
#         print(f"get_news: {get_news}")
#         search_term = data["search_term"].lower()
#         print(f"Search term received: {search_term}")

#         # save search term in search history if it is not already there
#         search_history = SearchHistory.objects.filter(search_term=search_term).first()
#         if not search_history:
#             SearchHistory.objects.create(search_term=search_term,user=request.user)
#             print("search history created")


#         # get or create search_term
#         try:
#             search_tag = SearchTag.objects.get(tag_name__iexact=search_term)
#         except SearchTag.DoesNotExist:
#             search_tag = SearchTag.objects.create(tag_name=search_term)
#         except SearchTag.MultipleObjectsReturned:
#             search_tag = SearchTag.objects.filter(tag_name__iexact=search_term).first()
#         print(f"Search tag created: {search_tag}")
#         # filter search tag into search options
#         if search_tag and get_news == False:
#             # find search options with this tag

#             if search_tag.options.exists():
#                 # return search options
#                 data = []
#                 for option in search_tag.options.all():
#                     data.append(
#                         {
#                             "search_tag": search_tag.tag_name,
#                             "keyword": option.keyword,
#                             "category": option.category,
#                             "subcategory": option.subcategory,
#                         }
#                     )
#                 response_data = {
#                     "code": status.HTTP_200_OK,
#                     "success": True,
#                     "message": "Search options fetched successfully",
#                     "data": data,
#                 }
#                 return Response(response_data, status=status.HTTP_200_OK)
#             else:
#                 # create search options
#                 try:
#                     generate_options = search_bar(search_term, allow_options=True)[1]
#                     print(
#                         f"Generated search options: {generate_options} its type {type(generate_options)}"
#                     )
#                     if generate_options:
#                         for option in generate_options.values():
#                             print(option["key_words"])
#                             print(option["category"])
#                             SearchOption.objects.create(
#                                 search_tag=search_tag,
#                                 keyword=option["key_words"],
#                                 category=option["category"],
#                                 subcategory=option["subcatetgory"],
#                             )
#                         generated_data = [{
#                             "search_tag": search_tag.tag_name,
#                             "keyword": option.keyword,
#                             "category": option.category,
#                             "subcategory": option.subcategory,
#                         } for option in search_tag.options.all()]
#                         print("all the generated data: ", generated_data)
#                         response_data = {
#                             "code": status.HTTP_201_CREATED,
#                             "success": True,
#                             "message": "Search options created successfully",
#                             "data": generated_data,
#                         }
#                         return Response(response_data, status=status.HTTP_200_OK)
#                 except Exception as e:
#                     print(f"Error generating search options: {e}")

#         elif search_tag and get_news == True:
#             # generate news
#             get_news = search_bar(search_term, allow_options=False)[1]
#             print(f"get_news: {get_news}")
#             # save the news to database
#             category, created = Category.objects.get_or_create(category_name=get_news["category"]["categorie_name"])
#             subcategory, created = Subcategory.objects.get_or_create(subcategory_name=get_news["subcatetgory"]["subcatetgory_name"])
#             topic, created = Topic.objects.get_or_create(name=get_news["topic"]["name"])

#             search_news = Search.objects.create(
#                 category=category,
#                 subcategory=subcategory,
#                 general_fact=get_news["general_facts"],
#                 topic=topic,
#                 news=get_news["news"],
#                 interesting_trivia=get_news["interesting_trivia"],
#                 opinion=get_news["opinions"],
#                 question=get_news["questions"],
#                 further_key_words=get_news["further_key_words"],

#             )

#             response_data = {
#                 "code": status.HTTP_200_OK,
#                 "success": True,
#                 "message": "News fetched successfully",
#                 "data": model_to_dict(search_news),
#             }
#             return Response(response_data, status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_404_NOT_FOUND)


class SearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        get_news = data.get("get_news", False)
        search_term = data.get("search_term", "").lower()

        print(f"get_news: {get_news}")
        print(f"Search term received: {search_term}")

        if not search_term:
            return Response({
                "code": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Search term is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Save search history if not already saved
        if not SearchHistory.objects.filter(search_term=search_term).exists():
            try:
                SearchHistory.objects.create(search_term=search_term, user=request.user)
                print("Search history created")
            except Exception as e:
                print(f"Error saving search history: {e}")
                pass

        # Get or create search tag
        try:
            search_tag = SearchTag.objects.get(tag_name__iexact=search_term)
        except SearchTag.DoesNotExist:
            search_tag = SearchTag.objects.create(tag_name=search_term)
        except SearchTag.MultipleObjectsReturned:
            search_tag = SearchTag.objects.filter(tag_name__iexact=search_term).first()

        print(f"Search tag: {search_tag}")

        # ====> CASE 1: Return or create search options
        if search_tag and not get_news:
            if search_tag.options.exists():
                options_data = [
                    {
                        "search_tag": search_tag.tag_name,
                        "keyword": option.keyword,
                        "category": option.category,
                        "subcategory": option.subcategory,
                    }
                    for option in search_tag.options.all()
                ]
                return Response({
                    "code": status.HTTP_200_OK,
                    "success": True,
                    "message": "Search options fetched successfully",
                    "data": options_data,
                }, status=status.HTTP_200_OK)
            else:
                try:
                    _, generate_options = search_bar(search_term, allow_options=True)
                    print("Generated options:", generate_options)

                    for option in generate_options.values():
                        SearchOption.objects.create(
                            search_tag=search_tag,
                            keyword=option.get("key_words", ""),
                            category=option.get("category", ""),
                            subcategory=option.get("subcategory", ""),
                        )

                    generated_data = [
                        {
                            "search_tag": search_tag.tag_name,
                            "keyword": option.keyword,
                            "category": option.category,
                            "subcategory": option.subcategory,
                        }
                        for option in search_tag.options.all()
                    ]

                    return Response({
                        "code": status.HTTP_201_CREATED,
                        "success": True,
                        "message": "Search options created successfully",
                        "data": generated_data,
                    }, status=status.HTTP_200_OK)

                except Exception as e:
                    print("Error generating options:", traceback.format_exc())
                    return Response({
                        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "success": False,
                        "message": f"Error generating options: {str(e)}"
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # ====> CASE 2: Generate and return news
        elif search_tag and get_news:
            try:
                _, get_news_data = search_bar(search_term, allow_options=False)
                print("Raw get_news_data:", get_news_data)

                # Validate keys
                required_keys = ["category", "subcategory", "topic", "general_facts", "news", "interesting_trivia", "opinions", "questions", "further_key_words"]
                for key in required_keys:
                    if key not in get_news_data:
                        raise ValueError(f"Missing key in get_news_data: '{key}'")

                category_data = get_news_data["category"]
                subcategory_data = get_news_data["subcategory"]
                topic_data = get_news_data["topic"]

                category_name = category_data.get("category_name")
                subcategory_name = subcategory_data.get("subcategory_name")
                topic_name = topic_data.get("name")

                if not category_name or not subcategory_name or not topic_name:
                    raise ValueError("Missing category/subcategory/topic names")

                category, _ = Category.objects.get_or_create(category_name=category_name)
                subcategory, _ = Subcategory.objects.get_or_create(subcategory_name=subcategory_name)
                topic, _ = Topic.objects.get_or_create(name=topic_name)

                # Create Search (News) object
                search_news = Search.objects.create(
                    category=category,
                    subcategory=subcategory,
                    general_fact=get_news_data["general_facts"],
                    topic=topic,
                    news=get_news_data["news"],
                    interesting_trivia=get_news_data["interesting_trivia"],
                    opinion=get_news_data["opinions"],
                    question=get_news_data["questions"],
                    further_key_words=get_news_data["further_key_words"],
                )

                return Response({
                    "code": status.HTTP_200_OK,
                    "success": True,
                    "message": "News fetched successfully",
                    "data": model_to_dict(search_news),
                }, status=status.HTTP_200_OK)

            except Exception as e:
                print("Error generating news:\n", traceback.format_exc())
                return Response({
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "success": False,
                    "message": f"Error generating news: {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Default fallback
        return Response({
            "code": status.HTTP_404_NOT_FOUND,
            "success": False,
            "message": "Search data not found."
        }, status=status.HTTP_404_NOT_FOUND)


class SearchHistoryAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        search_history = SearchHistory.objects.filter(user=user)
        data = [{"id": history.id, "search_term": history.search_term} for history in search_history]
        return Response({
            "code": status.HTTP_200_OK,
            "success": True,
            "message": "Search history fetched successfully",
            "data": data,
        }, status=status.HTTP_200_OK)
