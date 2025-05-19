from rest_framework import serializers
from .models import Interest, UserInterests
from .gnews_service import human_readable_time  # import the time formatter
from datetime import datetime, timedelta

# class NotificationSerializer(serializers.ModelSerializer):
#     actor_name = serializers.SerializerMethodField()
#     actor_image = serializers.SerializerMethodField()
#     time_display = serializers.SerializerMethodField()
#     is_new = serializers.SerializerMethodField()

#     class Meta:
#         model = Notification
#         fields = [
#             'id', 'notif_type', 'category', 'actor_name', 'actor_image',
#             'post_title', 'post_image', 'message', 'icon_url',
#             'is_read', 'is_new', 'time_display'
#         ]

#     def get_actor_name(self, obj):
#         return obj.actor_user.get_full_name() if obj.actor_user else None

#     def get_actor_image(self, obj):
#         return obj.actor_user.profile.image.url if obj.actor_user and hasattr(obj.actor_user, 'profile') else None

#     def get_time_display(self, obj):
#         return human_readable_time(obj.created_at)

#     def get_is_new(self, obj):
#         return not obj.is_read and obj.created_at.date() == datetime.today().date()
    
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
