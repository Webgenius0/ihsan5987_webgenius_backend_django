from django.urls import path
from .views import SignupView, VerifyOTPView, ResendOTPView, LoginView, ResetPasswordView, ForgotPasswordView

app_name = 'users'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend_otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('signin/', LoginView.as_view(), name='signin'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
]
