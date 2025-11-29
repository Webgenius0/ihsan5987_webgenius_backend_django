from rest_framework import serializers
from .models import (
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
    class Meta:
        model = Recommendation
        fields = "__all__"


class UserPreferenceSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()
    class Meta:
        model = Preference
        # fields = ['id', 'user', 'category', 'subcategory']
        exclude = ['created_at', 'updated_at']
        
    def get_category(self, obj):
        categories = obj.category.all()
        return [{'id': category.id, 'name': category.category_name} for category in categories]

    def get_subcategory(self, obj):
        subcategories = obj.subcategory.all()
        return [{'id': subcategory.id, 'name': subcategory.subcategory_name} for subcategory in subcategories]