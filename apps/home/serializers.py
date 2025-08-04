from rest_framework import serializers
from .models import (
    Topic,
    Category,
    Subcategory,
    Search,
    UpdateMe,
    Trending,
    Recommendation,
    Preference,
)
from apps.profiles.models import Feedback
from apps.users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "category_name"]


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ["id", "subcategory_name"]


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
    # search = SearchSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ["id", "user", "content", "rating", "created_at"]


class UpdateMeSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True, source='category_id')
    # subcategory = SubcategorySerializer(read_only=True, source='subcategory_id')
    # topic = TopicSerializer(read_only=True, source='topic_id')

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
    class Meta:
        model = Recommendation
        fields = "__all__"


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "user"]

    def create(self, validated_data):
        user = self.context["request"].user
        category = validated_data.pop("category")
        subcategory = validated_data.pop("subcategory")

        # get or create user preferences
        preference, created = Preference.objects.get_or_create(user=user)
        if category:
            preference.category.set(category)
        if subcategory:
            preference.subcategory.set(subcategory)
        preference.save()
        return preference
