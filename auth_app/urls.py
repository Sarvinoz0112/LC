from django.urls import path
from .views import (
    LoginAPIView, LogoutView, CurrentUserView, ChangePasswordView,
    ResetPasswordView, VerifyOTPView, SetNewPasswordView
)

app_name = "auth"

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
]
