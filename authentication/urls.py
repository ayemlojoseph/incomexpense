from django.urls import path
from .views import RegisterView, SetNewPasswordAPIView, VerifyEmail, LoginAPIView, PasswordTokenCheckAPI, RequestPasswordResetEmail

#refresh token import
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    #urls for refreshing token when it expires based on the lifespan we set in settings.py with JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), #url for requesting password change
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', #url for reseting the password
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),#url after reset is complete
         name='password-reset-complete')
]


