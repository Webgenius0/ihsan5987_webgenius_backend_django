from rest_framework import serializers
from .models import (
    Response, Topic, Category, Subcategory, GeneralFact, News, InterestingTrivia,
    Opinion, Question, Search, UpdateMe, Trending, Recommendation, Preference
)
from apps.profiles.models import Feedback
from apps.users.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'subcategory_name']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        # fields = ['id', 'name', 'topic_tags', 'created_at']
        fields = '__all__'

class GeneralFactSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralFact
        fields = [
            'id', 'general_definition', 'general_points', 'general_fun_fact', 'general_created_at',
            'key_facts_text', 'key_facts_fun_fact', 'key_facts_created_at',
            'picture_url', 'picture_created_at'
        ]

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'id', 'news_text', 'news_fun_facts',
            'news_oldest_article_date', 'news_newest_article_date',
            'news_picture_url', 'news_picture_created_at'
        ]

class InterestingTriviaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestingTrivia
        fields = [
            'id', 'trivia_text', 'picture_url',
            'trivia_fun_fact', 'trivia_text_created_at', 'trivia_picture_created_at'
        ]

class OpinionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opinion
        fields = ['id', 'opinions_text', 'opinions_fun_fact', 'opinions_created_at']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'questions_text', 'questions_fun_fact', 'questions_created_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'avatar_url', 'premium_status', 'created_at']

class ResponseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, source='category_id')
    subcategory = SubcategorySerializer(read_only=True, source='subcategory_id')
    topic = TopicSerializer(read_only=True, source='topic_id')
    general_fact = GeneralFactSerializer(read_only=True, source='general_facts_id')
    news = NewsSerializer(read_only=True, source='news_id')
    interesting_trivia = InterestingTriviaSerializer(read_only=True, source='interesting_trivia_id')
    opinion = OpinionSerializer(read_only=True, source='opinions_id')
    question = QuestionSerializer(read_only=True, source='questions_id')

    class Meta:
        model = Response
        fields = [
            'id', 'category', 'subcategory', 'topic', 'general_fact', 'news',
            'interesting_trivia', 'opinion', 'question', 'further_key_words', 'created_at'
        ]

class SearchSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    response = ResponseSerializer(read_only=True, source='response_id')

    class Meta:
        model = Search
        fields = ['id', 'user', 'search_term', 'response', 'options_id', 'created_at']

class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    search = SearchSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'search', 'content', 'rating', 'created_at']


class UpdateMeSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True, source='category_id')
    # subcategory = SubcategorySerializer(read_only=True, source='subcategory_id')
    # topic = TopicSerializer(read_only=True, source='topic_id')

    class Meta:
        model = UpdateMe
        # fields = '__all__'
        exclude = ['user']
        depth = 1

class TrendingNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trending
        fields = '__all__'
        depth = 1

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'

class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'user']
    
    def create(self, validated_data):
        user = self.context['request'].user
        category = validated_data.pop('category')
        subcategory = validated_data.pop('subcategory')
        
        # get or create user preferences
        preference, created = Preference.objects.get_or_create(user=user)
        if category:
            preference.category.set(category)
        if subcategory:
            preference.subcategory.set(subcategory)
        preference.save()
        return preference