from rest_framework import serializers
from .models import Interest, UserInterests, TrendingNews, RecommendedNews, NewsBookmark
from .gnews_service import human_readable_time  # import the time formatter
from datetime import datetime, timedelta

#Trending news serializer
class TrendingNewsSerializer(serializers.ModelSerializer):
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = TrendingNews
        fields = '__all__'

    def get_is_bookmarked(self, obj):
        user = self.context.get('request').user
        return obj.bookmarks.filter(user=user).exists()
    
#Recommended news serializer
class RecommendedNewsSerializer(serializers.ModelSerializer):
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = RecommendedNews
        fields = '__all__'

    def get_is_bookmarked(self, obj):
        user = self.context.get('request').user
        return obj.bookmarks.filter(user=user).exists()


#Bookmark news serializer
class NewsBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsBookmark
        fields = ['id', 'user', 'article', 'bookmarked_at']
        read_only_fields = ['user', 'bookmarked_at']


#User interests serializer
class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ('id', 'name')

class UserInterestsSerializer(serializers.ModelSerializer):
    interests = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    selected_interests = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserInterests
        fields = ('id', 'user', 'interests', 'selected_interests')
        read_only_fields = ('user', 'selected_interests')

    def validate_interests(self, value):
        if len(value) > 8:
            raise serializers.ValidationError("You can only select up to 8 interests.")

        # Validate that all names exist in the DB
        missing = []
        for name in value:
            if not Interest.objects.filter(name__iexact=name).exists():
                missing.append(name)
        if missing:
            raise serializers.ValidationError(f"Invalid interests: {', '.join(missing)}")
        return value

    def create(self, validated_data):
        names = validated_data.pop('interests', [])
        user = self.context['request'].user

        interest_objs = Interest.objects.filter(name__in=names)

        user_interests, _ = UserInterests.objects.get_or_create(user=user)
        user_interests.selected_interests = interest_objs.count()
        user_interests.save()
        user_interests.interests.set(interest_objs)
        return user_interests

    def update(self, instance, validated_data):
        names = validated_data.pop('interests', [])
        interest_objs = Interest.objects.filter(name__in=names)

        instance.selected_interests = interest_objs.count()
        instance.save()
        instance.interests.set(interest_objs)
        return instance


# class UserInterestsSerializer(serializers.ModelSerializer):
#     user_interests = InterestSerializer(many=True, read_only=True)

#     class Meta:
#         model = UserInterests
#         fields = ('id', 'user', 'user_interests', 'selected_interests')
#         read_only_fields = ('user', 'user_interests') # Make sure the user field is read-only and not editable

#     def validate_interests(self, value):
#         if len(value) > 8:
#             raise serializers.ValidationError("You can only select up to 8 interests.")
#         return value

#     def create(self, validated_data):
#         interests = validated_data.pop('interests', [])
#         user = self.context['request'].user

#         instance, _ = UserInterests.objects.get_or_create(user=user)
#         instance.selected_interests = len(interests)
#         instance.save()
#         instance.interests.set(interests)
#         return instance

#     def update(self, instance, validated_data):
#         interests = validated_data.pop('interests', [])
#         instance.selected_interests = len(interests)
#         instance.save()
#         instance.interests.set(interests)
#         return instance
