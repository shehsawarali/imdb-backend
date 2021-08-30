from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import LoginAPI, RegistrationAPI, VerifySession

urlpatterns = [
    path("login/", LoginAPI.as_view()),
    path("session/", VerifySession.as_view()),
    path("register/", RegistrationAPI.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
