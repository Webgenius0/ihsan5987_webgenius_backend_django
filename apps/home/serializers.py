from rest_framework import serializers
from .models import (
    Topic,
    Category,
    Subcategory,
    UpdateMe,
    Trending,
    Recommendation,
    Preference,
)
from apps.profiles.models import Feedback
from apps.users.models import User

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'subcategory_name']


class CategorySerializer(serializers.ModelSerializer):
    # show subcategories through relationship
    subcategories = SubcategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'subcategories']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        # fields = ['id', 'name', 'topic_tags', 'created_at']
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "bio",
            "avatar_url",
            "premium_status",
            "created_at",
        ]


class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ["id", "user", "content", "rating", "created_at"]


class UpdateMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateMe
        # fields = '__all__'
        exclude = ["user"]
        depth = 1


class TrendingNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trending
        fields = "__all__"
        depth = 1


class RecommendationSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    subcategory = serializers.StringRelatedField()
    topic = serializers.StringRelatedField()
    class Meta:
        model = Recommendation
        fields = "__all__"


class UserPreferenceSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    category = CategorySerializer(many=True, read_only=True)
    # subcategory = SubcategorySerializer(many=True, read_only=True)
    class Meta:
        model = Preference
        # fields = ['id', 'user', 'category', 'subcategory']
        exclude = ['subcategory', 'created_at', 'updated_at']
