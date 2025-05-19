# apps/users/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .models import BlacklistToken
from rest_framework import status

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)

        if result is None:
            return None
        
        user, validated_token = result

        jti = validated_token.get('jti')

        if jti and BlacklistToken.objects.filter(jti=jti).exists():
            raise AuthenticationFailed({
                'status': status.HTTP_401_UNAUTHORIZED,
                'success': False,
                'error': 'Token blacklisted. Please login again.',
            })
        
        return user, validated_token
    

   