from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import User

#Signup Serializer
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'confirm_password')
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
        
        validate_password(data["password"])
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User.objects.create_user(**validated_data)
        return user
from django.contrib.auth.hashers import check_password
#Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        if not check_password(data['password'], user.password):
            raise serializers.ValidationError("Invalid email or password.")

        # Don't check is_active here — let the view handle it
        data['user'] = user
        return data
