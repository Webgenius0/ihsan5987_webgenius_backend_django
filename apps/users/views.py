import random
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import login
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, EmailOTP
from django.conf import settings
from .serializers import SignupSerializer, LoginSerializer


#Signup View
class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)

            otp = str(random.randint(1000, 9999))

            
            EmailOTP.objects.create(
                user=user,
                otp=otp,
                created_at=timezone.now(),
                attempts=0
            )

            # Send OTP email
            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP is {otp}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )

            response_data = {
                "status": status.HTTP_201_CREATED,
                "success": "true",
                "message": "User created. OTP sent to email for verification.",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        response_data = {
            "status": status.HTTP_400_BAD_REQUEST,
            "success": "false",
            "message": serializer.errors,
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

#Verify OTP View
class VerifyOTPView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            user = User.objects.get(email=email)
            otp_obj = EmailOTP.objects.filter(user=user, is_verified=False).latest('created_at')
        except EmailOTP.DoesNotExist:
            response_data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "success": "false",
                "message": "No active OTP found. Please request a new one.",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": "false",
                "message": "User not found.",
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check OTP expiration (3 minutes)
        if otp_obj.is_expired():
            otp_obj.delete()
            response_data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "success": "false",
                "message": "OTP has expired. Please resend OTP.",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        
        if not otp_obj.has_attempts_left():
            otp_obj.delete()
            return Response({
                "status": status.HTTP_403_FORBIDDEN,
                "success": "false",
                "message": "Maximum attempts exceeded. Please resend OTP.",
            }, status=status.HTTP_403_FORBIDDEN)

        if otp != otp_obj.otp:
            otp_obj.attempts += 1
            otp_obj.save()
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": "false",
                "message": f"Incorrect OTP. Attempts left: {max(0, 3 - otp_obj.attempts)}"
            }, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()

        otp_obj.is_verified = True
        otp_obj.delete()

        response_data = {
            "status": status.HTTP_200_OK,
            "success": "true",
            "message": "OTP verified successfully.",
        }
        return Response(response_data, status=status.HTTP_200_OK)


#Verify Reset Password OTP View
class VerifyResetPasswordOTPView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            user = User.objects.get(email=email, is_active = True)
            otp_obj = EmailOTP.objects.filter(user=user, is_verified=False).latest('created_at')
        except EmailOTP.DoesNotExist:
            response_data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "success": "false",
                "message": "No active OTP found. Please request a new one.",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": "false",
                "message": "User not found.",
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check OTP expiration (3 minutes)
        if otp_obj.is_expired():
            otp_obj.delete()
            response_data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "success": "false",
                "message": "OTP has expired. Please resend OTP.",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        
        if not otp_obj.has_attempts_left():
            otp_obj.delete()
            return Response({
                "status": status.HTTP_403_FORBIDDEN,
                "success": "false",
                "message": "Maximum attempts exceeded. Please resend OTP.",
            }, status=status.HTTP_403_FORBIDDEN)

        if otp != otp_obj.otp:
            otp_obj.attempts += 1
            otp_obj.save()
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": "false",
                "message": f"Incorrect OTP. Attempts left: {max(0, 3 - otp_obj.attempts)}"
            }, status=status.HTTP_400_BAD_REQUEST)

        otp_obj.is_verified = True
        otp_obj.save()

        response_data = {
            "status": status.HTTP_200_OK,
            "success": "true",
            "message": "OTP verified successfully.",
        }
        return Response(response_data, status=status.HTTP_200_OK)

#Resend OTP View
class ResendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')

        # Check if email is provided
        if not email:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid credentials.",
                "errors": "Email is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success": False,
                    "message": "Invalid credentials.",
                    "errors": "User is already verified."
                }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid credentials.",
                "errors": "User does not exist."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Reset OTP attempts if user is eligible
        try:
            otp_obj = EmailOTP.objects.filter(user=user, is_verified=False).latest('created_at')
            # Update existing OTP
            otp = str(random.randint(1000, 9999))
            otp_obj.otp = otp
            otp_obj.created_at = timezone.now()
            otp_obj.attempts = 0  # Reset attempts
            otp_obj.save()
        except EmailOTP.DoesNotExist:
            # No existing OTP found, create a new one
            otp = str(random.randint(1000, 9999))
            EmailOTP.objects.create(
                user=user,
                otp=otp,
                created_at=timezone.now(),
                attempts=0
            )

        send_mail(
            subject="Resend OTP Code",
            message=f"Your new OTP is {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "OTP resent successfully.",
        }   
        return Response(response_data, status=status.HTTP_200_OK)
    
#Forgot Password View
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Email is required."
            }, status = status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            response_data = {
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "User with this email does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        otp = str(random.randint(1000, 9999))
        EmailOTP.objects.filter(user=user).delete()
        EmailOTP.objects.create(
            user=user, 
            otp=otp, 
            created_at=timezone.now(),
            attempts=0
        )

        send_mail(
            subject="Your Password Reset OTP",
            message=f"Your OTP is {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "OTP sent to your email."
        }, status = status.HTTP_200_OK)

#Reset Password View
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not email or not otp or not new_password or not confirm_password:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Email, OTP, new password, and confirm password are required."
            }, status = status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Passwords do not match."
            }, status = status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            otp_obj = EmailOTP.objects.filter(user=user, otp=otp, is_verified=True).latest('created_at')
        except (User.DoesNotExist, EmailOTP.DoesNotExist):
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "OTP not verified or user not found."
            }, status = status.HTTP_400_BAD_REQUEST)

        if otp_obj:
            user.set_password(new_password)
            user.save()

        EmailOTP.objects.filter(user=user).delete()  # Clean up OTPs

        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Password reset successfully."
        }, status=200)


#Login View
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            if not user.is_active:
                return Response(
                    {
                        "status": status.HTTP_403_FORBIDDEN,
                        "success": "false",
                        "message": "Account not verified. Please verify your email.",
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # response_data = {
            #         "status": status.HTTP_200_OK,
            #         "success": "true",
            #         "message": "Login Successful",
            #         "data": {
            #             "access_token": access_token,
            #             "refresh_token": str(refresh)
            #         },
            #     }
            response_data = {
                "access_token": access_token,
                "refresh_token": str(refresh)
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        error_message = None
        if 'errors' in serializer.errors:
            error_value = serializer.errors['errors']
            error_message = error_value[0] if isinstance(error_value, list) else error_value

        response_error = {
            "status": status.HTTP_400_BAD_REQUEST,
            "success": "false",
            "message": "Invalid login credentials",
            "errors": error_message,
        }
        return Response(response_error, status=status.HTTP_400_BAD_REQUEST)

# Logout API
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data["refresh_token"]
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Logout successful",
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except refresh_token.DoesNotExist: 
            response_data = {
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Refresh Token not found",
            }      
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
