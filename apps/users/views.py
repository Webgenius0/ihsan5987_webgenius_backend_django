import random
from django.utils import timezone
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.notifications.services import send_system_notification
from .models import User, EmailOTP, UserDevice
from django.conf import settings
from .serializers import SignupSerializer, LoginSerializer

# Signup View
class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)
            
            otp = str(random.randint(1000, 9999))

            # Send OTP email
            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP is {otp}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )

            EmailOTP.objects.create(
                user=user,
                otp=otp,
                created_at=timezone.now(),
                attempts=0
            )

            response_data = {
                "status": status.HTTP_201_CREATED,
                "success": "true",
                "message": f"User created. OTP sent to email for verification. {otp}",
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
        send_system_notification(
            recipient=user,
            title="Account Setup Complete",
            message="Your account has been successfully completed. Welcome aboard!",
            event_type='account_complete',
        )
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
            "message": "Reset Password OTP verified successfully.",
        }
        return Response(response_data, status=status.HTTP_200_OK)

# Resend Verify OTP View
class ResendVerifyOTPView(APIView):
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
    

# Resend Reset Password OTP View
class ResendResetOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid credentials.",
                "errors": "Email is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid credentials.",
                "errors": "User does not exist."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if EmailOTP.objects.filter(user=user, is_verified=True).exists():
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid request.",
                "errors": "Forget Password Resend OTP is already verified."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if user already has an unverified OTP
            otp_obj = EmailOTP.objects.filter(user=user, is_verified=False).latest('created_at')
            # If we find an unverified OTP, consider that the user is not verified yet
            # So we allow to resend
        except EmailOTP.DoesNotExist:
            otp_obj = None

        # Generate a new OTP or update the existing one
        otp = str(random.randint(1000, 9999))
        if otp_obj:
            otp_obj.otp = otp
            otp_obj.created_at = timezone.now()
            otp_obj.attempts = 0
            otp_obj.save()
        else:
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
        
        send_system_notification(
            recipient=user,
            title="Password Changed",
            message="Your password has been successfully changed.",
            event_type='password_change',
        )
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


            device_info = UserDevice.get_device_info(request)
            ip_address = UserDevice.get_client_ip(request)

            known_device = UserDevice.objects.filter(
                user=user, device_info=device_info, ip_address=ip_address
            ).first()

            if not known_device:
                UserDevice.objects.create(user=user, device_info=device_info, ip_address=ip_address)

                send_system_notification(
                    recipient=user,
                    title="New Device Login",
                    message="Your account was accessed from a new device. If this wasn't you, please secure your account.",
                    event_type='new_device_login',
                )

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Login Successful",
                "token_type": "Bearer",
                "token": access_token,
                "data": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "is_verified": user.is_active,
                    "is_subscribed": user.is_subscribed,
                },
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        error_message = None
        if 'errors' in serializer.errors:
            error_value = serializer.errors['errors']
            error_message = error_value[0] if isinstance(error_value, list) else error_value

        response_error = {
            "status": status.HTTP_403_FORBIDDEN,
            "success": False,
            "message": "Invalid login credentials",
            "errors": error_message,
        }
        return Response(response_error, status=status.HTTP_403_FORBIDDEN)
    

# Change Password View
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not current_password or not new_password or not confirm_password:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Current password, new password, and confirm password are required."
            }, status = status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(email=request.user.email)
        if not user.check_password(current_password):
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Current password is incorrect."
            }, status = status.HTTP_400_BAD_REQUEST)
        
        if new_password != confirm_password:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Passwords do not match."
            }, status = status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=request.user.email)
            user.set_password(new_password)
            user.save()
        except User.DoesNotExist:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "User not found."
            }, status = status.HTTP_400_BAD_REQUEST)

        send_system_notification(
            recipient=user,
            title="Password Changed",
            message="Your account password has been successfully changed.",
            event_type='password_change',
        )

        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Password changed successfully."
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Logout successful."
        }, status=status.HTTP_200_OK)
        

