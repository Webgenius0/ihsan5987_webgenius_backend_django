from django.urls import path
from .views import SignupView, VerifyOTPView, ResendVerifyOTPView, ResendResetOTPView, LoginView, ProtectedView, ForgotPasswordView, VerifyResetPasswordOTPView, ResetPasswordView, ChangePasswordView, LogoutView

app_name = 'users'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend_verify_otp/', ResendVerifyOTPView.as_view(), name='resend_verify_otp'),
    path('resend_reset_otp/', ResendResetOTPView.as_view(), name='resend_reset_otp'),
    path('signin/', LoginView.as_view(), name='signin'),
    path('forget_password/', ForgotPasswordView.as_view(), name='forget_password'),
    path('verify_reset_otp/', VerifyResetPasswordOTPView.as_view(), name='verify_reset_password_otp'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('protect_view/', ProtectedView.as_view(), name='protected_view'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
