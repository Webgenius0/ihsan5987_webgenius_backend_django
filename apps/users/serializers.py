from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils.timezone import now
from apps.notifications.services import send_system_notification
from rest_framework import status
from .models import User

#Signup Serializer
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ('name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        # Use create_user to properly hash the password
        return User.objects.create_user(**validated_data)
    
#Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"errors": ["Invalid credentials."]})
    
        user_instance = authenticate(email=email, password=password)

        if user_instance:
            # Reset on success
            user.failed_login_attempts = 0
            user.last_failed_login = None
            user.save()
            data['user'] = user
            return data

        # Failed login
        user.failed_login_attempts += 1
        user.last_failed_login = now()
        user.save()

        # Optional system notification
        if user.failed_login_attempts >= 3:
            send_system_notification(
                recipient=user,
                title="⚠️ Multiple Wrong Password Attempts",
                message="There have been multiple failed login attempts. If this wasn't you, consider changing your password.",
                event_type='wrong_password',
            )
        raise serializers.ValidationError({"errors": ["Invalid credentials."]})
