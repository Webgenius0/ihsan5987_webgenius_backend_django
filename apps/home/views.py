from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import (
    Response as ResponseModel, Topic, Category, Subcategory, GeneralFact, News,
    InterestingTrivia, Opinion, Question, Search
)
from apps.users.models import User
from apps.profiles.models import Feedback
from .serializers import (
    ResponseSerializer, TopicSerializer, CategorySerializer, SubcategorySerializer,
    GeneralFactSerializer, NewsSerializer, InterestingTriviaSerializer, OpinionSerializer,
    QuestionSerializer, UserSerializer, SearchSerializer, FeedbackSerializer
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
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
        category_id = request.query_params.get('category_id')
        topic_id = request.query_params.get('topic_id')

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
        user_id = request.query_params.get('user_id')
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
        user_id = request.query_params.get('user_id')
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


from .get_data import get_update_me, get_recommendations
from .models import UpdateMeUser

from rest_framework.exceptions import ValidationError


class UpdateMeAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        my_sub_ctg = ["Football", "Basketball", "Tennis"]
        data = get_update_me(my_sub_ctg)

        print("update me data", data) 

        # save response into database
        # check if the same title data already exist in database.
        for item in data:
            # if UpdateMe.objects.filter(topic__name=item['topic']).exists():
            #     print("Update Me data already exists.")
            #     continue
            # else:
            try:
                update = UpdateMe.objects.create(
                    category= Category.objects.get_or_create(category_name__icontains=item['category'])[0],
                    subcategory=Subcategory.objects.get_or_create(subcategory_name__icontains=item['subcategory'])[0],
                    topic=Topic.objects.get_or_create(name=item['topic'])[0],
                    short_info=item['short_info'],
                    reference_url=item['reference_url'],
                    background_story=item['background_story'],
                    picture_url=item['picture_url']
                )
                # create update me user
                UpdateMeUser.objects.create(
                    user=request.user,
                    update_me=update
                )
            except Exception as e:
                raise ValidationError(e)

            
            print("Update Me data saved successfully.")
            
        return Response({
            "status": "success",
            "data": data
        })


class RecommandationAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        my_sub_ctg = ["Football", "Basketball", "Tennis"]

        recommendations = get_recommendations(my_sub_ctg)

        print("recommendations", recommendations)

        # save response into database
        # check if the same title data already exist in database.

        for item in recommendations:
            try:
                recommendation = Recommendation.objects.create(
                    # user=request.user,
                    category=Category.objects.get_or_create(
                        category_name__icontains=item["category"]
                    )[0],
                    topic=Topic.objects.get_or_create(name=item["topic"])[0],
                    headline=item["headline"],
                    introduction=item["introduction"],
                    key_tips_and_takeaways=item["key_tips_and_takeaways"],
                    fun_facts=item["fun_facts"],
                    conclusion=item["conclusion"],
                    picture_url=item["image_url"],
                )
                # create recommendation user
                # RecommendationUser.objects.create(
                #     user=request.user,
                #     recommendation=recommendation
                # )
            except Exception as e:
                raise ValidationError(e)
        return Response({
            "status": "success",
            "data": recommendations
        })


# import requests
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.conf import settings
# from rest_framework.permissions import IsAuthenticated
# from apps.community_hubs.models import Post
# from apps.community_hubs.serializers import PostlistSerializer
# from django.shortcuts import get_object_or_404


# # Trending News API


# #Community Hub API
# class CommunityHubAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         posts = Post.objects.all().order_by("-created_at")

#         serializer = PostlistSerializer(posts, many=True)
#         return Response({
#             "status": status.HTTP_200_OK,
#             "success": True,
#             "message": "Posts fetched successfully",
#             "data": serializer.data
#         })

# #Search News API
# class SearchResultsAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         query = request.query_params.get('q')
#         if not query:
#             return Response({"error": "Query parameter 'q' is required"}, status=400)

#         url = "https://gnews.io/api/v4/search"
#         params = {
#             'q': query,
#             'lang': 'en',
#             'max': 10,
#             'token': settings.GNEWS_API_KEY
#         }
#         res = requests.get(url, params=params)
#         if res.status_code == 200:
#             response_data = {
#                 'status': status.HTTP_200_OK,
#                 'success': True,
#                 'message': 'Search results fetched successfully',
#                 'data': res.json().get('articles', [])
#             }
#             return Response(response_data, status = status.HTTP_200_OK)
#         else:
#             response_data = {
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'success': False,
#                 'message': 'Search failed',
#                 'errors': res.json()
#             }
#             return Response(response_data, status = status.HTTP_400_BAD_REQUEST)

# #Update Me API
# class UpdateMeAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         categories = ['general', 'world', 'nation', 'business', 'technology', 'entertainment', 'sports', 'science', 'health', 'politics']

#         update = []

#         for category in categories:
#             params = {
#                 'token': settings.GNEWS_API_KEY,
#                 'lang': 'en',
#                 'country': 'us',
#                 'max': 10,
#                 'q': category
#             }

#             response = requests.get("https://gnews.io/api/v4/search", params=params)

#             if response.status_code == 200:
#                 articles = response.json().get('articles', [])
#                 for article in articles:
#                     update.append({
#                         'title': article.get('title'),
#                         'description': article.get('description'),
#                         'content': article.get('content'),
#                         'url': article.get('url'),
#                         'image': article.get('image'),
#                         'publishedAt': article.get('publishedAt'),
#                         'source': {
#                             'name': article.get('source', {}).get('name'),
#                             'url': article.get('source', {}).get('url'),
#                         },
#                         'category': category  # manually tagged category
#                     })
#         response_data = {
#             'status': status.HTTP_200_OK,
#             'success': True,
#             'message': 'Update news fetched successfully',
#             'data': update
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

# #Posts View API
# class PostsAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         query = request.GET.get('q')

#         if query:
#             # Use search endpoint when query is present
#             url = "https://gnews.io/api/v4/search"
#             params = {
#                 'q': query,
#                 'token': settings.GNEWS_API_KEY,
#                 'lang': 'en',
#                 'max': 10
#             }
#         else:
#             # Use top-headlines endpoint when query is not present
#             url = "https://gnews.io/api/v4/top-headlines"
#             params = {
#                 'token': settings.GNEWS_API_KEY,
#                 'lang': 'en',
#                 'country': 'us',
#                 'max': 10
#             }

#         response = requests.get(url, params=params)

#         if response.status_code == 200:
#             response_data = {
#                 'status': status.HTTP_200_OK,
#                 'success': True,
#                 'message': 'Posts fetched successfully',
#                 'data': response.json().get('articles', [])
#             }
#             return Response(response_data, status=status.HTTP_200_OK)
#         response_data = {
#             'status': status.HTTP_400_BAD_REQUEST,
#             'success': False,
#             'message': 'Failed to fetch posts',
#             'errors': response.json()
#         }
#         return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# #Your News API
# class YourNewsAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         url = "https://gnews.io/api/v4/top-headlines"
#         params = {
#             'token': settings.GNEWS_API_KEY,
#             'lang': 'en',
#             'country': 'us',
#             'max': 10
#         }

#         response = requests.get(url, params=params)
#         if response.status_code == 200:
#             response_data = {
#                 'status': status.HTTP_200_OK,
#                 'success': True,
#                 'message': 'Your news fetched successfully',
#                 'data': response.json().get('articles', [])
#             }
#             return Response(response_data, status=status.HTTP_200_OK)
#         response_data = {
#             'status': status.HTTP_400_BAD_REQUEST,
#             'success': False,
#             'message': 'Failed to fetch your news',
#             'errors': response.json()
#         }
#         return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# #Your Interests API
# class YourInterestAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         interests = request.GET.getlist('topics')  # list of interests

#         if not interests:
#             return Response({'error': 'Please provide at least one topic using ?topics=topic1&topics=topic2'})

#         all_articles = []
#         for topic in interests:
#             url = "https://gnews.io/api/v4/search"
#             params = {
#                 'q': topic,
#                 'token': settings.GNEWS_API_KEY,
#                 'lang': 'en',
#                 'max': 3  # limit per topic
#             }
#             response = requests.get(url, params=params)
#             if response.status_code == 200:
#                 all_articles.extend(response.json().get('articles', []))
#                 response_data = {
#                     'status': status.HTTP_200_OK,
#                     'success': True,
#                     'message': 'Your interests fetched successfully',
#                     'data': all_articles
#                 }
#                 return Response(response_data, status=status.HTTP_200_OK)
#             response_data = {
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 'success': False,
#                 'message': 'Failed to fetch your interests',
#                 'errors': response.json()
#             }
#             return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


# #User interests API
from decouple import config
from datetime import date
from rest_framework.permissions import AllowAny

from utility.ai_scripts import (
    generate_update_element,
    generate_trending_now_element,
    recommendations
)

from .models import (
    UpdateMe,   
    Trending,
    Recommendation,
    Preference
)
from .serializers import (
    UpdateMeSerializer,
    TrendingNewsSerializer,
    RecommendationSerializer
)

openai_api_key = config("OPENAI_API_KEY")
class UpdateMeAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        update_me_data = UpdateMe.objects.all().order_by('-created_at')
        serializer = UpdateMeSerializer(update_me_data, many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Update Me data fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
    

    def post(self, request):
        try:
            data = generate_update_element("Israel Palestine War",openai_api_key)

            if data:
                print("Generated data:", data)

                topic_title = data.get("topic")
                category_name = data.get("category")
                subcategory_name = data.get("subcategory")
                topic_title = data.get("topic")
                short_info = data.get("short_info", [])
                reference_url = data.get("reference_url")
                background_story = data.get("background_story", {})
                picture_url = data.get("picture_url")

                # Fetch or create related models
                category, _ = Category.objects.get_or_create(category_name=category_name)
                subcategory, _ = Subcategory.objects.get_or_create(subcategory_name=subcategory_name)
                topic, _ = Topic.objects.get_or_create(name=topic_title)

                # Save the update
                update = UpdateMe.objects.create(
                    user_id=1,  # Replace with the correct user ID or logic
                    category=category,
                    subcategory=subcategory,
                    topic=topic,
                    short_info=short_info,
                    reference_url=reference_url,
                    background_story=background_story,
                    picture_url=picture_url,
                    created_at=date.today(),
                    interest=True
                )
            print('message is saved')
        except Exception as e:
            print(f"Error saving update me data: {e}")
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": "Failed to save Update Me data"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Update Me data saved successfully"
        }, status=status.HTTP_200_OK)


class TrendingNewsAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = generate_trending_now_element("world cup football", openai_api_key)
            if data:
                print("generated data", data)
                # example ai response
                # {{
                #     "topic": "Super Bowl 2025",
                #     "category": "Sports",
                #     "subcategory": "NFL",
                #     "description": "Super Bowl 2025 is the most anticipated event of the year, drawing millions of viewers worldwide.",
                #     "why_is_it_trending": [
                #         "The game is just days away, and preparations are in full swing.",
                #         "High-profile teams are expected to deliver a thrilling performance.",
                #         "The halftime show lineup, headlined by Kendrick Lamar, is generating buzz."
                #     ],
                #     "key_points": [
                #         "Teams: Philadelphia Eagles vs. Kansas City Chiefs.",
                #         "Halftime Show: Star performances with potential surprise guests.",
                #         "Betting Odds: Significant shifts in favor of an underdog."
                #     ],
                #     "overlook_what_might_happen_next": [
                #         "Game Prediction: Analysts lean towards a close contest.",
                #         "Halftime Surprises: There may be unexpected guest performances.",
                #         "Viewership: Could set new records in streaming numbers."
                #     ]
                #     }}

                # topic_title = data.get("topic")
                category_name = data.get("category")
                subcategory_name = data.get("subcategory")
                description = data.get("description")
                why_is_it_trending = data.get("why_is_it_trending", [])
                key_points = data.get("key_points", [])
                overlook_what_might_happen_next = data.get("overlook_what_might_happen_next", [])
                picture_url = data.get("picture_url")

                category, _ = Category.objects.get_or_create(category_name=category_name)
                subcategory, _ = Subcategory.objects.get_or_create(subcategory_name=subcategory_name)


                trending_model = Trending.objects.create(
                    # key_words=topic_title,
                    category=category,
                    subcategory=subcategory,
                    description=description,
                    why_trending=why_is_it_trending,
                    key_points=key_points,
                    outlook=overlook_what_might_happen_next,
                    picture_url=picture_url,
                    created_at=date.today()
                )
                print("Trending news saved successfully.")
                return Response({
                    "status": status.HTTP_201_CREATED,
                    "success": True,
                    "message": "Trending news data saved successfully",
                    "data": {
                        "id": trending_model.id,
                        "category": category_name,
                        "subcategory": subcategory_name,
                        "description": description,
                        "why_trending": why_is_it_trending,
                        "key_points": key_points,
                        "outlook": overlook_what_might_happen_next,
                        "picture_url": picture_url
                    }
                }, status=status.HTTP_201_CREATED)
            else:
                print("No data generated.")
        except Exception as e:
            print(f"Error saving trending news data: {e}")
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": "Failed to save trending news data"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        trending_news = Trending.objects.all().order_by('-created_at')
        serializer = TrendingNewsSerializer(trending_news, many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Trending news data fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class RecommendationsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        recommendations_data = Recommendation.objects.all().order_by('-created_at')
        serializer = RecommendationSerializer(recommendations_data, many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Recommendations data fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            data = recommendations("world cup football", OPENAI_API_KEY=openai_api_key)
            if data:
                print("Generated data:", data)

                topic_title = data.get("topic")
                category_name = data.get("category")

                topic, _ = Topic.objects.get_or_create(name=topic_title)
                category, _ = Category.objects.get_or_create(category_name=category_name)

                recommendation_model = Recommendation.objects.create(
                    user_id=1,  # Replace with the correct user ID or logic
                    category=category,
                    topic=topic,
                    headline=data.get("headline", ""),
                    introduction=data.get("introduction", ""),
                    key_tips_and_takeaways=data.get("key_tips_and_takeaways", ""),
                    fun_facts=data.get("fun_facts", ""),
                    conclusion=data.get("conclusion", ""),
                    picture_url=data.get("picture_url",None),
                    created_at=date.today(),
                    last_refresh=date.today()
                )
                print('message is saved')

            else:
                print("No data generated.")
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "message": "Failed to generate recommendations"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Recommendations data generated successfully",
            "data": data
        }, status=status.HTTP_200_OK)

class PreferencesAPIView(APIView):
    # permission_classes = [AllowAny]

    def post(self, request):
        user = request.user
        data = request.data.get('interests',[])
        print('data', data)

        for name in data:
            category = Category.objects.filter(category_name__icontains=name).first()
            print('category', category)
            if category:
                # Update or create the user's preference for this category
                user_preferences, _ = Preference.objects.get_or_create(
                    user=user,
                    category=category,
                )     
                print('add preferences')
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Preferences updated successfully"
        }, status=status.HTTP_200_OK)
